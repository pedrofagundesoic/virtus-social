# meta-token.ps1 - turn the short-lived Explorer token into: long-lived user token, PAGE token (never expires), IG_USER_ID.
# Usage (PowerShell):  .\scripts\meta-token.ps1 -EnvFile "$env:USERPROFILE\.social.env"
# Reads FB_APP_ID, FB_APP_SECRET, FB_PAGE_ID, FB_USER_TOKEN_SHORT from the env file; writes the derived values back.
param([string]$EnvFile = "$env:USERPROFILE\.social.env")
$ErrorActionPreference = 'Stop'
$G = 'https://graph.facebook.com/v21.0'
$kv = @{}; Get-Content $EnvFile | Where-Object { $_ -match '^\s*([A-Z_]+)=(.*)$' } | ForEach-Object { $kv[$matches[1]] = ($matches[2] -replace '\s+#.*$','').Trim() }
foreach ($k in 'FB_APP_ID','FB_APP_SECRET','FB_PAGE_ID','FB_USER_TOKEN_SHORT') { if (-not $kv[$k]) { throw "missing $k in $EnvFile" } }

Write-Host "1) exchanging for a long-lived user token..."
$ll = Invoke-RestMethod "$G/oauth/access_token?grant_type=fb_exchange_token&client_id=$($kv.FB_APP_ID)&client_secret=$($kv.FB_APP_SECRET)&fb_exchange_token=$($kv.FB_USER_TOKEN_SHORT)"
$long = $ll.access_token

Write-Host "2) fetching the Page token DIRECTLY (do not rely on /me/accounts)..."
$pg = Invoke-RestMethod "$G/$($kv.FB_PAGE_ID)?fields=access_token,name,instagram_business_account&access_token=$long"
if (-not $pg.access_token) { throw "no page token - redo the OAuth grant choosing 'only current Pages' and tick the Page" }
$igId = $pg.instagram_business_account.id
if (-not $igId) { Write-Warning "instagram_business_account empty: link the IG business account to the Page and make sure instagram_basic is in the grant" }

Write-Host "3) verifying..."
$me = Invoke-RestMethod "$G/me?access_token=$($pg.access_token)"
$dbg = Invoke-RestMethod "$G/debug_token?input_token=$($pg.access_token)&access_token=$($kv.FB_APP_ID)|$($kv.FB_APP_SECRET)"
Write-Host ("   page   : {0} ({1})" -f $me.name, $me.id)
Write-Host ("   expires: {0}  (0 = never)" -f $dbg.data.expires_at)
Write-Host ("   scopes : {0}" -f ($dbg.data.scopes -join ','))
if ($igId) { $ig = Invoke-RestMethod "$G/$($igId)?fields=username&access_token=$($pg.access_token)"; Write-Host ("   IG     : @{0} ({1})" -f $ig.username, $igId) }

function Set-EnvLine([string]$k, [string]$v) {
  $lines = @(Get-Content $EnvFile)
  if ($lines -match "^$k=") { $lines = $lines -replace "^$k=.*$", "$k=$v" } else { $lines += "$k=$v" }
  Set-Content $EnvFile $lines -Encoding utf8
}
Set-EnvLine 'FB_USER_TOKEN_LONGLIVED' $long
Set-EnvLine 'FB_PAGE_TOKEN' $pg.access_token
if ($igId) { Set-EnvLine 'IG_USER_ID' $igId }
Write-Host "written to $EnvFile - now copy FB_PAGE_ID, FB_PAGE_TOKEN, IG_USER_ID to the GitHub repo Secrets."
