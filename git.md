# Git Usage Guide
## วิธีใช้ Git

## Table of Contents
- [Clone](#clone)
- [Push](#push)
- [Pull](#pull)
- [Checkout](#checkout)
- [Branch](#branch)
- [Merge](#merge)
- [Log & Diff](#log--diff)
- [Reset & Revert](#reset--revert)
- [Stash](#stash)
- [Tag](#tag)
- [Remote](#remote)
- [Configure](#configure)
- [Useful Commands](#useful-commands)

---

## Clone
#### ดึงโค้ดจาก GitHub หรือ GitLab
```bash
git clone <git-url>
```

---

## Push
#### ส่งโค้ดขึ้น Git
```bash
# ตรวจสอบสถานะ / Check status
git status

# เพิ่มไฟล์ / Add files
git add <file1> <file2> ...   # เพิ่มทีละไฟล์ / Add each file
git add -A                    # เพิ่มทุกไฟล์ / Add all files
git add *.py                  # เพิ่มไฟล์ที่ตรง pattern / Add files matching pattern

# Commit / บันทึกการเปลี่ยนแปลง
git commit -m "<message>"

# Push ขึ้น Git
git push
git push origin <branch-name>  # Push ไปยัง specific branch
```

---

## Pull
#### ดึงโค้ดจาก Git
```bash
git pull
git pull origin <branch-name>  # Pull จาก specific branch
```

---

## Checkout
#### เปลี่ยน Branch
```bash
git checkout <branch-name>

# แตก Branch ใหม่ / Create new branch
git checkout -b <branch-name>
```

---

## Branch
#### จัดการ Branch
```bash
# แสดงรายการ Branch / List branches
git branch                    # Local branches
git branch -a                 # ทั้งหมด (local + remote)
git branch -r                 # Remote branches

# แตก Branch ใหม่ (ไม่สลับไปใช้) / Create new branch
git branch <branch-name>

# ลบ Branch / Delete branch
git branch -d <branch-name>   # ลบถ้า merge แล้ว
git branch -D <branch-name>   # บังคับลบ / Force delete

# เปลี่ยนชื่อ Branch / Rename branch
git branch -m <new-name>      # Branch ปัจจุบัน
git branch -m <old-name> <new-name>  # เปลี่ยนชื่อเฉพาะ
```

---

## Merge
#### รวม Branch
```bash
# Merge branch อื่นเข้ามา
git checkout <target-branch>
git merge <source-branch>

# Merge แบบ no-fast-forward (เก็บ merge commit)
git merge --no-ff <source-branch>

# ยกเลิก merge / Abort merge
git merge --abort
```

---

## Log & Diff
#### ดูประวัติและการเปลี่ยนแปลง
```bash
# ดูประวัติ commit / View commit history
git log
git log --oneline             # แบบย่อ / Short format
git log --oneline --graph     # แสดง graph
git log --all --graph         # ทุก branch

# ดูการเปลี่ยนแปลง / View changes
git diff                      # การเปลี่ยนแปลงที่ยังไม่ได้ add
git diff --staged             # การเปลี่ยนแปลงที่ add แล้ว แต่ยังไม่ได้ commit
git diff <commit1> <commit2>  # เปรียบเทียบระหว่าง commits

# ดูรายละเอียด commit
git show <commit-hash>

# ดูประวัติของไฟล์ / View file history
git log -- <file-path>
```

---

## Reset & Revert
#### ย้อนกลับการเปลี่ยนแปลง
```bash
# Soft reset (เก็บการเปลี่ยนแปลงใน staging)
git reset --soft <commit-hash>

# Mixed reset (เก็บใน working directory)
git reset --mixed <commit-hash>

# Hard reset (ลบการเปลี่ยนแปลงทั้งหมด)
git reset --hard <commit-hash>

# Revert (สร้าง commit ใหม่เพื่อย้อนกลับ)
git revert <commit-hash>
```

---

## Stash
#### เก็บการเปลี่ยนแปลงชั่วคราว
```bash
# เก็บการเปลี่ยนแปลง / Stash changes
git stash
git stash save "message"      # พร้อมข้อความ

# ดูรายการ stash / List stashes
git stash list

# นำ stash กลับมา / Apply stash
git stash pop                 # Apply และลบออก
git stash apply               # Apply แต่ไม่ลบ

# ใช้ stash เฉพาะ
git stash apply stash@{0}

# ลบ stash / Delete stash
git stash drop stash@{0}
git stash clear               # ลบทั้งหมด
```

---

## Tag
#### กำหนด Tag
```bash
# แสดงรายการ tag / List tags
git tag

# สร้าง tag ใหม่ / Create tag
git tag <tag-name>
git tag -a v1.0 -m "Version 1.0"  # Annotated tag

# Push tag ขึ้น remote
git push origin <tag-name>
git push origin --tags        # Push ทุก tag

# Checkout ที่ tag
git checkout <tag-name>
```

---

## Remote
#### จัดการ Remote
```bash
# แสดงรายการ remote / List remotes
git remote -v

# เพิ่ม remote / Add remote
git remote add origin <git-url>

# เปลี่ยน remote URL
git remote set-url origin <new-git-url>

# ลบ remote / Remove remote
git remote remove origin

# ดูสถานะ remote
git remote show origin
```

---

## Configure
#### การตั้งค่า Git
```bash
# ตั้งค่า user / User configuration
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# ดูการตั้งค่า / View configuration
git config --global --list

# Cache credentials (จำรหัสผ่าน)
git config credential.helper store

# ปิด Vim mode (เมื่อ commit ต้องใส่ message)
git config --global core.editor "nano"
# หรือ
git config --global core.editor "code --wait"

# ปิด SSL verification (ไม่แนะนำสำหรับ production)
git config --global http.sslVerify false

# Line ending settings (สำหรับ Windows)
git config --global core.autocrlf true
```

---

## Useful Commands
#### คำสั่งอื่นๆ ที่มีประโยชน์
```bash
# ดูสถานะแบบย่อ / Short status
git status -s

# ดู commit ล่าสุด / Last commit
git log -1

# ดู commit ล่าสุด 5 ตัว / Last 5 commits
git log -5 --oneline

# สร้าง .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore

# ดูขนาดของ repository
git count-objects -vH

# Clean ไฟล์ที่ไม่ถูก track / ลบ untracked files
git clean -n                  # ดูว่าจะลบอะไร (preview)
git clean -f                  # ลบเลย / Delete
git clean -fd                 # ลบไฟล์และ directory
```

---

## Git Flow (พื้นฐาน)
#### ขั้นตอนการทำงานแบบพื้นฐาน
```bash
# 1. ดึงโค้ดล่าสุด
git pull origin main

# 2. แตก branch ใหม่สำหรับงาน
git checkout -b feature/my-feature

# 3. ทำงานและ commit
git add .
git commit -m "feat: add new feature"

# 4. Push branch ขึ้น remote
git push origin feature/my-feature

# 5. Merge กลับ main (ทำผ่าน Pull Request)
git checkout main
git pull origin main
git merge feature/my-feature
git push origin main
```

---

## References
- [Git Official Documentation](https://git-scm.com/doc)
- [StackOverflow - Git Credentials](https://stackoverflow.com/questions/5343068/is-there-a-way-to-cache-https-credentials-for-pushing-commits)