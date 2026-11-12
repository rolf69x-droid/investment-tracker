# My Investment Tracker — Android-friendly PWA

This is a real installable, mobile-friendly web app, not an Excel workbook. It tracks the three funds and uses locally saved units. It includes a dashboard, a daily history table, and a portfolio history chart.

## What works now
- Dashboard, local unit entry, portfolio arithmetic, chart and history rendering.
- A Python daily NAV collector that validates ISIN, NAV and published NAV date from public Raiffeisen fund pages.
- A GitHub Actions workflow to collect prices and commit daily history after deployment.
- No Excel, macros, or running PC required after hosting is configured.

## Important limitations
- **Not yet deployed or live.** `data/history.json` starts empty. The app shows no live prices until the collector successfully runs.
- Public website HTML can change or block automated access; this has not been verified live here. The collector deliberately fails without overwriting history if parsing fails.
- The default GitHub schedule is 16:10 **winter** / 17:10 **summer** Italian time. GitHub schedules use UTC, and scheduled workflows can run late or be skipped. Change cron to `10 14 * * 1-5` for 16:10 summer. For exact year-round 16:00, use an external timezone-aware scheduler.
- Data history stored in a public GitHub Pages repo is **public**. It includes fund NAVs but not your unit holdings, which stay in the browser's local storage. Do not add account details or personal financial information to the repo.
- Historical portfolio totals are recalculated using current units, not a record of past holdings. To calculate true investment returns, purchase prices and transactions are needed.
- This app doesn't track purchase cost, realized gains, or distributions yet.

## Deploy (one-time, requires a GitHub account)
1. Create a new GitHub repository, upload these files including `.github/workflows/daily.yml` and `data/history.json`.
2. Enable GitHub Pages from the repository's `main` branch, root folder.
3. Under Actions, run **Collect daily fund NAVs** manually once. If it succeeds, the app will display your prices. If it fails, inspect the workflow log; the Raiffeisen website may have changed.
4. Open the Pages URL on Android in Chrome, then choose **Add to Home screen** / **Install app**.
5. Enter your units under **My units**. Initial defaults are the three unit quantities previously supplied.

For private hosted history, use private hosting with authenticated access rather than public GitHub Pages.
