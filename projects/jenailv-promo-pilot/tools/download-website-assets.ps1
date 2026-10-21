$ErrorActionPreference = 'Stop'

function Get-SharedSha256([string]$Path) {
    $stream = [IO.File]::Open($Path, [IO.FileMode]::Open, [IO.FileAccess]::Read, [IO.FileShare]::ReadWrite)
    try {
        $sha = [Security.Cryptography.SHA256]::Create()
        try { return ([BitConverter]::ToString($sha.ComputeHash($stream))).Replace('-', '') }
        finally { $sha.Dispose() }
    }
    finally { $stream.Dispose() }
}

$projectRoot = Split-Path -Parent $PSScriptRoot
$websiteRoot = Join-Path $projectRoot 'references\website'
$rawHtml = Join-Path $websiteRoot 'home.html'
$assetRoot = Join-Path $projectRoot 'assets\source\website'
$manifestPath = Join-Path $websiteRoot 'download-manifest-v001.csv'

if (-not (Test-Path -LiteralPath $rawHtml)) { throw "Missing archived homepage: $rawHtml" }
New-Item -ItemType Directory -Force -Path $assetRoot | Out-Null

$html = Get-Content -LiteralPath $rawHtml -Raw -Encoding utf8
$seen = @{}
$rows = [System.Collections.Generic.List[object]]::new()
$order = 0

foreach ($match in [regex]::Matches($html, '<img[^>]+>', 'IgnoreCase')) {
    $tag = $match.Value
    $src = [regex]::Match($tag, 'src=["'']([^"'']+)', 'IgnoreCase').Groups[1].Value
    $alt = [regex]::Match($tag, 'alt=["'']([^"'']*)', 'IgnoreCase').Groups[1].Value
    if (-not $src -or $seen.ContainsKey($src)) { continue }
    if ($src -match '/tel\.png$|/more1\.png$|1790470290480468\.png$') { continue }
    if ($src -notmatch '/static/upload/image/|/skin/images/pic1\.jpg$|/skin/images/lc[1-7]\.png$') { continue }

    $seen[$src] = $true
    $order++
    $uri = if ($src -match '^https?://') { $src } else { "https://www.jenailv.net$src" }
    $baseName = [IO.Path]::GetFileName(([uri]$uri).AbsolutePath)
    $localName = ('{0:D3}-{1}' -f $order, $baseName)
    $localPath = Join-Path $assetRoot $localName
    if ((-not (Test-Path -LiteralPath $localPath)) -or ((Get-Item -LiteralPath $localPath).Length -eq 0)) {
        $tempPath = "$localPath.part"
        Remove-Item -LiteralPath $tempPath -Force -ErrorAction SilentlyContinue
        & curl.exe -L --fail --retry 3 --connect-timeout 15 --max-time 90 -A 'Mozilla/5.0' $uri -o $tempPath
        if ($LASTEXITCODE -ne 0) { throw "Download failed: $uri" }
        if ((Get-Item -LiteralPath $tempPath).Length -eq 0) { throw "Empty download: $uri" }
        Move-Item -LiteralPath $tempPath -Destination $localPath -Force
    }
    try { $hash = Get-SharedSha256 $localPath }
    catch { $hash = 'pending_file_lock' }
    $category = if ($order -eq 1) {'brand'} `
        elseif ($order -le 4) {'hero'} `
        elseif ($order -eq 5) {'factory'} `
        elseif ($order -le 11) {'product'} `
        elseif ($order -le 17) {'case'} `
        elseif ($order -le 27) {'factory'} `
        elseif ($order -le 34) {'process'} `
        else {'news'}
    $rows.Add([pscustomobject]@{
        download_order = $order
        category = $category
        label = $alt
        source_url = $uri
        local_file = "assets/source/website/$localName"
        sha256 = $hash
        rights_status = 'user_confirmed_authorized_for_case'
        review_status = 'not_visually_reviewed'
    })
}

$rows | Export-Csv -LiteralPath $manifestPath -NoTypeInformation -Encoding utf8
Write-Output "Downloaded $($rows.Count) assets"
Write-Output $manifestPath
