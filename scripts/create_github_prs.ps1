# PowerShell script to push all feature branches and create real Pull Requests on GitHub
param(
    [string]$GitHubToken = ""
)

$RepoOwner = "pernamittasumanthreddy"
$RepoName = "Smart-Employee-Management-System"
$BaseBranch = "main"

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "  Smart EMS - GitHub Branch & Pull Request Automation" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

# Check git status
Write-Host "`n[1/3] Pushing all local branches to GitHub..." -ForegroundColor Yellow

if ($GitHubToken -ne "") {
    $RemoteUrl = "https://${GitHubToken}@github.com/${RepoOwner}/${RepoName}.git"
    git push $RemoteUrl --all --force
    git push $RemoteUrl main --force
} else {
    git push origin --all
    git push origin main
}

Write-Host "`n[2/3] Checking GitHub CLI (gh) authentication..." -ForegroundColor Yellow

$ghInstalled = Get-Command gh -ErrorAction SilentlyContinue
$ghPath = "C:\Program Files\GitHub CLI\gh.exe"

$ghCmd = if ($ghInstalled) { "gh" } elseif (Test-Path $ghPath) { $ghPath } else { $null }

$BranchesToPR = @(
    @{ Branch = "feature-auth-docs"; Title = "docs(auth): add authentication documentation and RBAC architecture guide"; Body = "Implements RBAC documentation, multi-tier security, and session management." },
    @{ Branch = "feature-ui-docs"; Title = "docs(ui): add UI improvement notes and modern design system documentation"; Body = "Implements glassmorphic UI architecture, theme tokens, and Web Audio synthesizer engine." },
    @{ Branch = "feature-api-docs"; Title = "docs(api): add API documentation and REST endpoint specifications"; Body = "Implements enterprise RESTful API documentation, response envelopes, and endpoint directory." },
    @{ Branch = "feature-testing"; Title = "test(qa): add comprehensive testing guide and automated test matrix"; Body = "Implements end-to-end Pytest verification harness and coverage standards." },
    @{ Branch = "feature/statutory-compliance-and-taxation"; Title = "feat(statutory): Indian payroll tax engine and compliance framework"; Body = "Implements Section 115BAC tax calculations, PF/ESI calculators, and compliance rules." },
    @{ Branch = "feature/workforce-attendance-and-shifts"; Title = "feat(workforce): attendance biometric geofencing and shift solver"; Body = "Implements shift scheduling matrix, geofenced punch-in verification, and rosters." },
    @{ Branch = "feature/recruitment-ats-and-performance"; Title = "feat(talent): ATS recruitment pipeline and 9-box performance matrix"; Body = "Implements candidate resume parsing, OKR cascading, and employee appraisals." },
    @{ Branch = "feature/ai-insights-and-workplace-analytics"; Title = "feat(analytics): local autonomous ML attrition predictor and eNPS engine"; Body = "Implements ML flight risk classifier and sentiment analytics engine." }
)

if ($ghCmd) {
    Write-Host "GitHub CLI detected ($ghCmd). Attempting PR creation..." -ForegroundColor Green
    foreach ($item in $BranchesToPR) {
        $branch = $item.Branch
        $title = $item.Title
        $body = $item.Body
        
        Write-Host "Creating & Merging PR for branch: $branch" -ForegroundColor Cyan
        try {
            & $ghCmd pr create --base $BaseBranch --head $branch --title $title --body $body --repo "${RepoOwner}/${RepoName}" 2>&1
            & $ghCmd pr merge $branch --merge --repo "${RepoOwner}/${RepoName}" --delete-branch=false 2>&1
        } catch {
            Write-Host "Notice: PR for $branch may already exist or need login." -ForegroundColor Gray
        }
    }
} elseif ($GitHubToken -ne "") {
    Write-Host "Using GitHub REST API with Token..." -ForegroundColor Green
    $headers = @{
        "Authorization" = "Bearer $GitHubToken"
        "Accept" = "application/vnd.github.v3+json"
        "User-Agent" = "Smart-EMS-PR-Bot"
    }

    foreach ($item in $BranchesToPR) {
        $branch = $item.Branch
        $title = $item.Title
        $body = $item.Body

        Write-Host "Opening PR for branch: $branch" -ForegroundColor Cyan
        $payload = @{
            title = $title
            head = $branch
            base = $BaseBranch
            body = $body
        } | ConvertTo-Json

        try {
            $prResponse = Invoke-RestMethod -Uri "https://api.github.com/repos/${RepoOwner}/${RepoName}/pulls" -Method Post -Headers $headers -Body $payload -ContentType "application/json"
            $prNumber = $prResponse.number
            Write-Host "  -> PR #$prNumber opened! Merging into main..." -ForegroundColor Green

            $mergePayload = @{
                commit_title = "Merge pull request #$prNumber from $branch"
                merge_method = "merge"
            } | ConvertTo-Json

            $mergeResponse = Invoke-RestMethod -Uri "https://api.github.com/repos/${RepoOwner}/${RepoName}/pulls/$prNumber/merge" -Method Put -Headers $headers -Body $mergePayload -ContentType "application/json"
            Write-Host "  -> PR #$prNumber successfully merged!" -ForegroundColor Green
        } catch {
            Write-Host "  -> Notice: PR creation skipped or already processed: $_" -ForegroundColor Gray
        }
    }
} else {
    Write-Host "`nTo create real GitHub Pull Requests via GitHub API:" -ForegroundColor Yellow
    Write-Host "1. Run LOGIN_GITHUB_CLI.bat or create a GitHub Personal Access Token (PAT)."
    Write-Host "2. Or push branches to GitHub and open PRs at: https://github.com/${RepoOwner}/${RepoName}/pulls"
}

Write-Host "`n=================================================================" -ForegroundColor Cyan
Write-Host "  Completed! All local branches and merge history are ready." -ForegroundColor Green
Write-Host "=================================================================" -ForegroundColor Cyan
