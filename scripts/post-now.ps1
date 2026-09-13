# post-now.ps1 — manual test post straight to the Graph API (bypasses the publisher). Use ONCE for the first live test.
# Usage: .\scripts\post-now.ps1 -ImageUrl https://pedrofagundesoic.github.io/virtus-social/social/x.png -Caption "..." [-EnvFile ...] [-SkipIG]
param([Parameter(Mandatory)][string]$ImageUrl, [Parameter(Mandatory)][string]$Caption,
      [string]$EnvFile = "$env:USERPROFILE\.social.env", [switch]$SkipIG)
$ErrorActionPreference = 'Stop'; $G = 'https://graph.facebook.com/v21.0'
$kv = @{}; Get-Content $EnvFile | Where-Object { $_ -match '^\s*([A-Z_]+)=(.*)$' } | ForEach-Object { $kv[$matches[1]] = ($matches[2] -replace '\s+#.*$','').Trim() }
$t = $kv.FB_PAGE_TOKEN
$fb = Invoke-RestMethod -Method Post "$G/$($kv.FB_PAGE_ID)/photos" -Body @{ url = $ImageUrl; message = $Caption; access_token = $t }
Write-Host "FB post: https://www.facebook.com/$($fb.post_id)"
if ($SkipIG) { exit 0 }
$c = Invoke-RestMethod -Method Post "$G/$($kv.IG_USER_ID)/media" -Body @{ image_url = $ImageUrl; caption = $Caption; access_token = $t }
for ($i = 0; $i -lt 6; $i++) {
  $st = Invoke-RestMethod "$G/$($c.id)?fields=status_code&access_token=$t"
  if ($st.status_code -eq 'FINISHED') { break }; if ($st.status_code -eq 'ERROR') { throw 'IG container ERROR' }
  Start-Sleep 5
}
$p = Invoke-RestMethod -Method Post "$G/$($kv.IG_USER_ID)/media_publish" -Body @{ creation_id = $c.id; access_token = $t }
Write-Host "IG media id: $($p.id)"
