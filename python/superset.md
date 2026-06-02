# Apache Superset

## Table of Contents

- [How to Make a Dashboard Public](#how-to-make-a-dashboard-public)

---

## How to Make a Dashboard Public

Follow these steps to expose a dashboard to unauthenticated (public) users:

1. Log in as **Admin**.
2. Go to **Settings > List Roles**.
3. Delete the existing **Public** role.
4. Edit the **Gamma** role and add the following permissions:
   - `can explore json on Superset`
   - `can dashboard on Superset`
   - `all database access on all_database_access`
5. Copy the **Gamma** role and rename the copy to **Public**:
   - Check the box next to **Gamma**.
   - Click **Action > Copy Role**.
   - Rename the new role to `Public`.
6. Test by opening the dashboard in an incognito browser window.
