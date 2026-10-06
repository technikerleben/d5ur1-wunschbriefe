/* Individuelle Lernrückmeldung: Seite 1 persönliche Entwicklung,
   Seite 2 vollständiges Kompetenzraster und nachrangige Noteneinordnung. */
(function () {
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
  const clamp=(v,max)=>Math.min(max,Math.max(0,Number(v)||0));
  const countFor=pct=>Math.ceil(Math.max(0,Math.min(100,pct))*6/100);

  function printKey(){
    const n1=countFor(settings.grade1Perf);
    const r2=countFor(settings.grade2Reg),l2=countFor(settings.grade2Perf);
    const r3=countFor(settings.grade3Reg);
    const m4=countFor(settings.grade4Min),m5=countFor(settings.grade5Min);
    const rows=[
      {n:1,minimum:n1*3,condition:n1+" von 6 auf Leistungsstandard"},
      {n:2,minimum:l2*3+2*Math.max(0,r2-l2),
        condition:r2+" von 6 auf Regelstandard und "+l2+" von 6 auf Leistungsstandard"},
      {n:3,minimum:r3*2,condition:r3+" von 6 auf Regelstandard"},
      {n:4,minimum:m4,condition:m4+" von 6 auf Mindeststandard"},
      {n:5,minimum:m5,condition:m5+" von 6 auf Mindeststandard"},
      {n:6,minimum:0,condition:"Die Bedingung für Note 5 ist noch nicht erreicht"}
    ];
    // Die 0–3 Punkte pro Kriterium zeigen Lernentwicklung. Die Bedingungen
    // für Noten beziehen sich auf die Anzahl der erreichten Kompetenzstufen.
    return rows.map(row=>'<div class="print-key-cell print-key-grade-'+row.n+'">'+
      '<strong>'+gradeNames[row.n]+'</strong><span>'+
      (row.n===6?"":'mindestens '+row.minimum+' Grundpunkte möglich · ')+
      escapeHtml(row.condition)+'</span></div>').join("");
  }

  function renderRubric(){
    p("printRubricGrid").innerHTML=CRITERIA.map(criterion=>
      '<article class="print-rubric-card">'+
        '<h3>'+escapeHtml(criterion.title)+'</h3>'+
        '<div class="print-rubric-desc">'+escapeHtml(criterion.desc)+'</div>'+
        criterion.levels.map((description,level)=>
          '<div class="print-rubric-row">'+
          '<span class="print-rubric-num print-level-'+level+'">'+level+'</span>'+
          '<span>'+escapeHtml(description)+'</span></div>'
        ).join("")+
      '</article>'
    ).join("");
  }

  function renderPrint(){
    const child=current();
    if(!child)return;
    const assessment=metrics(child);
    const rows=CRITERIA.map((criterion,index)=>({
      criterion,index,level:clamp(child.levels[criterion.id],3)
    }));
    const extra=clamp(child.survey,2);
    const basic=rows.reduce((sum,row)=>sum+row.level,0);

    p("printName").textContent=child.name||"______________________";
    p("printClass").textContent=child.className||"5.3";
    p("printDate").textContent=child.date?child.date.split("-").reverse().join("."):"__________";
    p("printToday").textContent=new Date().toLocaleDateString("de-DE",{
      day:"2-digit",month:"2-digit",year:"numeric"
    });

    p("printRows").innerHTML=rows.map(row=>{
      const name=row.criterion.short;
      return '<tr><td>'+escapeHtml(name[0].toUpperCase()+name.slice(1))+
        '</td><td><span class="print-level-badge print-level-'+row.level+'">'+
        names[row.level]+'</span></td><td>'+row.level+' / 3</td></tr>';
    }).join("")+
      '<tr class="print-extra-row"><td>Umfrage (freiwillige Zusatzaufgabe)</td>'+
      '<td><span class="print-level-badge print-level-extra">'+
      ["Nicht genutzt","Passend genannt","Richtig erklärt"][extra]+
      '</span></td><td>'+extra+' / 2</td></tr>';

    const positives=rows.filter(r=>r.level>=1)
      .sort((a,b)=>b.level-a.level||a.index-b.index);
    const messages=[];
    if(positives.length){
      messages.push("Du kannst schon "+skills[positives[0].criterion.id]+".");
      if(positives.length>=2)
        messages.push("Das gelingt dir gut: "+strengths[positives[1].criterion.id]+".");
      if(positives.length>=3)
        messages.push("Man erkennt, dass du "+skills[positives[2].criterion.id]+" kannst.");
      if(positives.length<3)
        messages.push("Wir üben gemeinsam weiter. Jeder neue Schritt zählt.");
      if(extra===2)
        messages.push("Zusätzlich hast du ein Umfrageergebnis richtig erklärt.");
    }else{
      messages.push("Wir schauen gemeinsam auf deinen Wunschbrief.");
      messages.push("Wir üben die wichtigen Schritte in Ruhe zusammen.");
    }
    p("printStrengths").replaceChildren();
    messages.forEach(message=>{
      const node=document.createElement("p");node.textContent=message;
      p("printStrengths").appendChild(node);
    });
    const weakest=[...rows].sort((a,b)=>a.level-b.level||a.index-b.index)[0];
    p("printTipText").textContent=NEXT_STEPS[weakest.criterion.id];

    p("printWarning").classList.toggle("hidden",assessment.grade<=4);
    const comment=(child.teacherComment||"").trim();
    p("printCustom").classList.toggle("hidden",!comment);
    p("printCustom").textContent=comment?"Persönliche Rückmeldung: "+comment:"";

    renderRubric();
    p("printGradeKey").innerHTML=printKey();
    p("printGrade").textContent=gradeNames[assessment.grade]||String(assessment.grade);
    p("printPoints").textContent=String(basic+extra);
    p("printCore").textContent=basic+" / 18";
    p("printExtras").textContent=extra+" / 2";
  }

  const trigger=p("printFeedback");
  trigger.onclick=()=>{
    if(!current())return;
    syncTop();renderPrint();window.print();
  };
  window.addEventListener("beforeprint",renderPrint);
})();
