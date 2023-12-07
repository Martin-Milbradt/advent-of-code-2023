Set-Location $(Split-Path $MyInvocation.MyCommand.Path)
git fetch origin
git add .

$fileNames = Get-ChildItem -File | Select-Object -ExpandProperty Name

$day = 0
foreach ($fileName in $fileNames) {
    if ($fileName -match "^\d+") {
        $number = [int]$matches[0]
        if ($number -gt $day) {
            $day = $number
        }
    }
}

git commit -m "day $day"
git push --set-upstream gitlab main
git push --set-upstream origin main

# Create files for the next day
$dd = "{0:D2}" -f ++$day

Copy-Item -Path "00 - Template.py" -Destination "$dd.py"

New-Item -Path "data" -Name "$dd.txt"
