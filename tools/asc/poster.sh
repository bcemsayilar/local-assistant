#!/bin/bash
# poster.sh "Locale label" -> select locale in Media Manager, set poster frame to 1.5s
cd /tmp/claude-501; export TABMATCH=${TABMATCH:-apps/6826862284}
./sj.sh "var btn=[...document.querySelectorAll('button')].find(b=>/\\((U\\.S\\.|U\\.K\\.|Canada|Australia)\\)|Japanese|Chinese|Turkish/.test(b.innerText)&&b.getBoundingClientRect().top<500); if(btn) btn.click(); 'open'"; sleep 1
./sj.sh "var e=[...document.querySelectorAll('[role=menuitem],[role=option],li,a')].find(e=>e.innerText.trim()=='$1'); if(e){e.click();'picked'}else{'nomatch'}"; sleep 5
./sj.sh "var b=[...document.querySelectorAll('button')].find(b=>b.innerText.trim()=='Edit Poster Frame'); if(!b){'no poster button'}else{b.click();'dialog'}"; sleep 3
./sj.sh "[...document.querySelectorAll('video')].forEach(v=>{v.pause();v.currentTime=1.5;v.dispatchEvent(new Event('seeked',{bubbles:true}));v.dispatchEvent(new Event('timeupdate',{bubbles:true}));}); 'seek'"; sleep 2
./sj.sh "[...document.querySelectorAll('button')].filter(b=>b.innerText.trim()=='Set Poster Frame')[0].click(); 'set'"; sleep 2
./sj.sh "[...document.querySelectorAll('button')].filter(b=>b.innerText.trim()=='Done')[0].click(); 'done'"; sleep 4
