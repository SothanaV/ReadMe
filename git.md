# How to use git 
## วิธีการใช้ git

## Clone
#### เอา git จาก github หรือ gitlab
    git clone < git url/ลิงก์ของ git>
#
## Push
#### เอาโค้ดขึ้น git
    # check status / เช็คสถานะ
    git status

    # add file / เพิ่มไฟล์
    git add <file file ... >    ## add each file / เพิ่มแต่ละไฟล์
    git add -A                  ## add all / เพิ่มไฟล์ทั้งหมด

    # commit / บอกว่าไฟล์ที่เพิ่มทำอะไรไป
    git commit -m "<comment / คอมเมนต์>"

    # push to git / เอาไฟล์ขึ้น git
    git push
# 

## Pull
#### เอาโค้ดจากgit
    git pull
#

## Checkout
#### change branch / เปลี่ยน branch
    git checkout <branch name / ชื่อbranch>

    # New branch / แตกbranchใหม่
    git checkout -b <branch name / ชื่อbranch>

