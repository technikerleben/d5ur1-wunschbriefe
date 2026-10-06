/* Nur für die gedruckte individuelle Rückmeldung. */
(function(){
  const p=id=>document.getElementById(id);
  const skills={
    situation:"einen passenden Wunsch verständlich ausdrücken",
    aufbau:"wichtige Teile des Briefes richtig anordnen",
    freundlichkeit:"freundlich und respektvoll schreiben",
    begruendung:"einen passenden Grund für deinen Wunsch nennen",
    sprache:"verständliche Sätze schreiben",
    lesbarkeit:"deinen Brief lesbar gestalten"
  };
  const strengths={
    situation:"Dein Wunsch passt zur Schreibsituation",
    aufbau:"Dein Brief hat die wichtigen Teile",
    freundlichkeit:"Du schreibst passend und höflich",
    begruendung:"Du nennst einen Grund für deinen Wunsch",
    sprache:"Man kann deine Sätze verstehen",
    lesbarkeit:"Man kann deinen Brief lesen"
  };
  const names=["Noch nicht erreicht","Mindeststandard","Regelstandard","Leistungsstandard"];
  const gradeNames={1:"sehr gut (1)",2:"gut (2)",3:"befriedigend (3)",4:"ausreichend (4)",5:"mangelhaft (5)",6:"ungenügend (6)"};
  function requiredCount(percent){return Math.ceil(6*percent/100)}
  function gradingKey(){
    // Mindestpunktzahl ist notwendig, aber allein nicht hinreichend:
    // Maßgeblich ist die Verteilung der erreichten Kompetenzniveaus.
    const perf1=requiredCount(settings.grade1Perf);
    const reg2=requiredCount(settings.grade2Reg), perf2=requiredCount(settings.grade2Perf);
    const reg3=requiredCount(settings.grade3Reg);
    const min4=requiredCount(settings.grade4Min),min5=requiredCount(settings.grade5Min);
    const minPts2=3*perf2+2*Math.max(0,reg2-perf2);
    const rules=[
      [1,3*perf1,perf1+" × Leistungsstandard"],
      [2,minPts2,reg2+" × Regelstandard + "+perf2+" × Leistungsstandard"],
      [3,2*reg3,reg3+" × Regelstandard"],
      [4,min4,min4+" × Mindeststandard"],
      [5,min5,min5+" × Mindeststandard"],
      [6,0,"unter der Schwelle für Note 5"]
    ];
    return rules.map(([grade,minPoints,detail])=>
      '<div class="print-key-cell print-key-grade-'+grade+'">'+
      '<div class="print-key-grade">'+gradeNames[grade]+'</div>'+
      '<div class="print-key-condition">'+
      (grade===6?"":'<strong>ab '+minPoints+' Grundpunkten</strong> · ')+detail+
      '</div></div>'
    ).join("");
  }
  function between(value,max){return Math.min(max,Math.max(0,Number(value)||0))}
  function renderPrint(){
    const child=current();
    if(!child)return;
    const assessment=metrics(child);
    const rows=CRITERIA.map((criterion,index)=>({
      criterion,index,level:between(child.levels[criterion.id],3)
    }));
    const extras=between(child.survey,2);
    const core=rows.reduce((sum,row)=>sum+row.level,0);
    p("printName").textContent=child.name||"________________________";
    p("printClass").textContent=child.className||"5.3";
    p("printDate").textContent=child.date?child.date.split("-").reverse().join("."):"__________";

    p("printRows").innerHTML=rows.map(row=>{
      const title=row.criterion.short;
      return "<tr><td>"+escapeHtml(title[0].toUpperCase()+title.slice(1))+
        '</td><td><span class="print-level-badge print-level-'+row.level+'">'+
        names[row.level]+"</span></td><td>"+row.level+" / 3</td></tr>";
    }).join("")+'<tr><td>Umfrage (freiwilliger Zusatz)</td><td><span class="print-level-badge print-level-extra">'+
      ["Nicht genutzt","Teilweise passend","Passend genutzt und erklärt"][extras]+
      "</span></td><td>"+extras+" / 2</td></tr>";
    p("printGradeKey").innerHTML=gradingKey();

    const positive=rows.filter(row=>row.level>=1)
      .sort((a,b)=>b.level-a.level||a.index-b.index);
    const messages=[];
    if(positive.length){
      messages.push("Du kannst schon "+skills[positive[0].criterion.id]+".");
      if(positive.length>=2)
        messages.push("Das gelingt dir gut: "+strengths[positive[1].criterion.id]+".");
      if(positive.length>=3)
        messages.push("Man erkennt, dass du "+skills[positive[2].criterion.id]+" kannst.");
      if(positive.length<3)
        messages.push("Schritt für Schritt wirst du noch sicherer. Dabei unterstützen wir dich.");
    } else {
      messages.push("Wir schauen gemeinsam auf deinen Wunschbrief.");
      messages.push("Wir üben die wichtigsten Schritte jetzt in Ruhe zusammen.");
    }
    p("printStrengths").replaceChildren();
    messages.forEach(message=>{
      const para=document.createElement("p");
      para.textContent=message;
      p("printStrengths").appendChild(para);
    });

    const weakest=[...rows].sort((a,b)=>a.level-b.level||a.index-b.index)[0];
    p("printTipText").textContent=NEXT_STEPS[weakest.criterion.id];
    p("printWarning").classList.toggle("hidden",assessment.grade<=4);
    const comment=(child.teacherComment||"").trim();
    p("printCustom").classList.toggle("hidden",!comment);
    p("printCustom").textContent=comment?"Persönliche Rückmeldung: "+comment:"";
    p("printGrade").textContent=gradeNames[assessment.grade]||String(assessment.grade);
    p("printToday").textContent=new Date().toLocaleDateString("de-DE",{day:"2-digit",month:"2-digit",year:"numeric"});
    p("printPoints").textContent=String(core+extras);
    p("printCore").textContent=core+" / 18";
    p("printExtras").textContent=extras+" / 2";
  }
  const printButton=p("printFeedback");
  printButton.onclick=function(){
    if(!current())return;
    syncTop();
    renderPrint();
    window.print();
  };
  window.addEventListener("beforeprint",renderPrint);
})();