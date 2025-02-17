let statistic=document.getElementById("floatWindow")
statistic.addEventListener("click",(event)=>{
    event.preventDefault();
   document.getElementById("StatisticsWindow").style="display:block";
})
document.getElementById("StatisticsWindow").addEventListener("click",()=>{
    document.getElementById("StatisticsWindow").style="display:none";
})

