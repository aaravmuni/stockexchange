let sections = [];

document.querySelectorAll(".sectionselect").forEach(link =>
{   
    sections.push(link.dataset.section);
    link.addEventListener("click", (e)=>{
        e.preventDefault();
        const section = link.dataset.section;
        console.log("switched to: "+section);
        switchtosection(section);
    })
});

window.addEventListener("hashchange", ()=>{
    const section = window.location.hash.slice(1);
    if(section)switchtosection(section);
})

window.addEventListener("DOMContentLoaded",()=>{
    const section = window.location.hash.slice(1);
    switchtosection(section || "explore")
})

console.log(sections);

switchtosection("explore")

function switchtosection(sec)
{
    if(sections.includes(sec)){
    sections.forEach(section =>{
        const id = "#"+section;
        const s = document.querySelector(id);
        if(section == sec)
        {
            s.style.display = "block";
            window.location.hash = sec;
        }
        else
        {
            s.style.display = "none";
        }
    });}
    else
    {
        console.log("no section exists named: " + sec);
        switchtosection("explore");
    }
}