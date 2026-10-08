/* Individuelle Lernrückmeldung:
   Seite 1 = persönliche Kompetenzen, Stärken, Lernschritt und individuelle Note.
   Seite 2 = vollständiges Kompetenzraster und transparenter Punkteschlüssel. */
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
  const lrsSkills={sprache:"vollständige Sätze schreiben und passende Satzschlusszeichen setzen"};
  const lrsStrengths={sprache:"Deine Sätze sind vollständig und deine Satzschlusszeichen passen"};
  const names=["Nicht vorhanden","In Ansätzen vorhanden","Mindeststandard","Regelstandard","Leistungsstandard"];
  const gradeNames={1:"sehr gut (1)",2:"gut (2)",3:"befriedigend (3)",4:"ausreichend (4)",5:"mangelhaft (5)",6:"ungenügend (6)"};
  const clamp=(v,max)=>Math.min(max,Math.max(0,Number(v)||0));

  function printKey(){
    const rows=[
      {n:1,pct:"ab 87 %",range:"21–26 Punkte"},
      {n:2,pct:"ab 73 %",range:"18–20 Punkte"},
      {n:3,pct:"ab 59 %",range:"15–17 Punkte"},
      {n:4,pct:"ab 45 %",range:"11–14 Punkte"},
      {n:5,pct:"ab 18 %",range:"5–10 Punkte"},
      {n:6,pct:"unter 18 %",range:"0–4 Punkte"}
    ];
    return rows.map(row=>
      '<div class="print-key-cell print-key-grade-'+row.n+'">'+
        '<strong>'+gradeNames[row.n]+'</strong>'+
        '<span>'+row.pct+' von 24 Punkten · '+row.range+'</span>'+
      '</div>'
    ).join("");
  }

  function renderRubric(child){
    p("printRubricGrid").innerHTML=CRITERIA.map(base=>{
      const criterion=criterionForStudent(base,child);
      return '<article class="print-rubric-card">'+
        '<h3>'+escapeHtml(criterion.title)+'</h3>'+
        '<div class="print-rubric-desc">'+escapeHtml(criterion.desc)+'</div>'+
        criterion.levels.map((description,index)=>{
          const level=index;
          return '<div class="print-rubric-row">'+
            '<span class="print-rubric-num print-level-'+level+'">'+level+'</span>'+
            '<span>'+escapeHtml(description)+'</span>'+
          '</div>';
        }).join("")+
      '</article>';
    }).join("");
  }

  function renderPrint(){
    const child=current();
    if(!child)return;

    const assessment=metrics(child);
    const rows=CRITERIA.map((criterion,index)=>({
      criterion,index,level:clamp(child.levels[criterion.id]??0,4)
    }));
    const extra=clamp(child.survey,2);

    p("printName").textContent=child.name||"______________________";
    p("printClass").textContent=child.className||"5.3";
    p("printDate").textContent=child.date?child.date.split("-").reverse().join("."):"__________";
    p("printToday").textContent=new Date().toLocaleDateString("de-DE",{
      day:"2-digit",month:"2-digit",year:"numeric"
    });

    p("printRows").innerHTML=rows.map(row=>{
      const shown=criterionForStudent(row.criterion,child);
      const name=shown.short;
      return '<tr><td>'+escapeHtml(name[0].toUpperCase()+name.slice(1))+
        '</td><td><span class="print-level-badge print-level-'+row.level+'">'+
        names[row.level]+'</span></td><td>'+row.level+' / 4</td></tr>';
    }).join("")+
      '<tr class="print-extra-row"><td>Umfrage (freiwillige Zusatzaufgabe)</td>'+
      '<td><span class="print-level-badge print-level-extra">'+
      ["Nicht genutzt","Passend genannt","Richtig erklärt"][extra]+
      '</span></td><td>'+extra+' / 2</td></tr>';

    const positives=rows.filter(r=>r.level>=2)
      .sort((a,b)=>b.level-a.level||a.index-b.index);
    const messages=[];
    if(positives.length){
      messages.push("Du kannst schon "+((child.lrsNta&&lrsSkills[positives[0].criterion.id])||skills[positives[0].criterion.id])+".");
      if(positives.length>=2)
        messages.push("Das gelingt dir gut: "+((child.lrsNta&&lrsStrengths[positives[1].criterion.id])||strengths[positives[1].criterion.id])+".");
      if(positives.length>=3)
        messages.push("Man erkennt, dass du "+((child.lrsNta&&lrsSkills[positives[2].criterion.id])||skills[positives[2].criterion.id])+" kannst.");
      if(positives.length<3)
        messages.push("Wir üben gemeinsam weiter. Jeder neue Schritt zählt.");
      if(extra===2)
        messages.push("Zusätzlich hast du ein Umfrageergebnis richtig erklärt.");
    }else{
      const anyApproach=rows.some(r=>r.level===1);
      messages.push(anyApproach
        ? "Du hast erste Ansätze für deinen Wunschbrief gezeigt."
        : "Wir schauen gemeinsam, welche Schritte dir beim Schreiben helfen.");
      messages.push("Wir üben die wichtigen Schritte gemeinsam weiter.");
    }
    p("printStrengthsHeading").textContent=rows.some(r=>r.level>=1)?"Das kannst du schon":"Deine nächsten Lernschritte";
    p("printStrengths").replaceChildren();
    messages.forEach(message=>{
      const node=document.createElement("p");
      node.textContent=message;
      p("printStrengths").appendChild(node);
    });

    const showTip=assessment.grade>2;
    p("printTip").classList.toggle("hidden",!showTip);
    const weakest=[...rows].sort((a,b)=>a.level-b.level||a.index-b.index)[0];
    p("printTipText").textContent=showTip?nextStepForStudent(weakest.criterion,child):"";

    p("printWarning").classList.toggle("hidden",assessment.grade<=4);
    const comment=(child.teacherComment||"").trim();
    p("printCustom").classList.toggle("hidden",!comment);
    p("printCustom").textContent=comment?"Persönliche Rückmeldung: "+comment:"";

    p("printFrontPoints").textContent=String(assessment.total)+" Punkte";
    p("printFrontBonus").textContent=assessment.extra>0
      ? "("+assessment.core+" / 24 Grundpunkte + "+assessment.extra+" Bonus"+(assessment.extra===1?"punkt":"punkte")+")"
      : "("+assessment.core+" / 24 Grundpunkte)";
    p("printFrontGrade").textContent=gradeNames[assessment.grade]||String(assessment.grade);

    renderRubric(child);
    p("printGradeKey").innerHTML=printKey();
  }

  const trigger=p("printFeedback");
  trigger.onclick=()=>{
    if(!current())return;
    syncTop();
    renderPrint();
    window.print();
  };
  window.addEventListener("beforeprint",renderPrint);
})();
