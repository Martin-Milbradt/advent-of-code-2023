Set-Location $(Split-Path $MyInvocation.MyCommand.Path)
git fetch origin
git add .

$fileNames = Get-ChildItem -File | Select-Object -ExpandProperty Name

$highestNumber = 0
foreach ($fileName in $fileNames) {
    if ($fileName -match "^\d+") {
        $number = [int]$matches[0]
        if ($number -gt $highestNumber) {
            $highestNumber = $number
        }
    }
}

git commit -m "day $highestNumber"
git push --set-upstream gitlab main
git push --set-upstream origin main
