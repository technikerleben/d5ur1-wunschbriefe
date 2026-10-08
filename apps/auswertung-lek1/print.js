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
  const names=["Noch nicht erreicht","Mindeststandard","Regelstandard","Leistungsstandard"];
  const gradeNames={1:"sehr gut (1)",2:"gut (2)",3:"befriedigend (3)",4:"ausreichend (4)",5:"mangelhaft (5)",6:"ungenügend (6)"};
  const clamp=(v,max)=>Math.min(max,Math.max(0,Number(v)||0));
  const minPoints=pct=>Math.ceil(MAX_POINTS*pct/100);

  function printKey(){
    const mins={
      1:minPoints(GRADE_THRESHOLDS[1]),
      2:minPoints(GRADE_THRESHOLDS[2]),
      3:minPoints(GRADE_THRESHOLDS[3]),
      4:minPoints(GRADE_THRESHOLDS[4]),
      5:minPoints(GRADE_THRESHOLDS[5])
    };
    const rows=[
      {n:1,pct:"ab 87 %",range:mins[1]+"–"+MAX_POINTS+" Punkte"},
      {n:2,pct:"ab 73 %",range:mins[2]+"–"+(mins[1]-1)+" Punkte"},
      {n:3,pct:"ab 59 %",range:mins[3]+"–"+(mins[2]-1)+" Punkte"},
      {n:4,pct:"ab 45 %",range:mins[4]+"–"+(mins[3]-1)+" Punkte"},
      {n:5,pct:"ab 18 %",range:mins[5]+"–"+(mins[4]-1)+" Punkte"},
      {n:6,pct:"unter 18 %",range:"0–"+(mins[5]-1)+" Punkte"}
    ];
    return rows.map(row=>
      '<div class="print-key-cell print-key-grade-'+row.n+'">'+
        '<strong>'+gradeNames[row.n]+'</strong>'+
        '<span>'+row.pct+' · '+row.range+'</span>'+
      '</div>'
    ).join("");
  }

  function renderRubric(){
    p("printRubricGrid").innerHTML=CRITERIA.map(criterion=>
      '<article class="print-rubric-card">'+
        '<h3>'+escapeHtml(criterion.title)+'</h3>'+
        '<div class="print-rubric-desc">'+escapeHtml(criterion.desc)+'</div>'+
        criterion.levels.map((description,level)=>
          '<div class="print-rubric-row">'+
            '<span class="print-rubric-num print-level-'+level+'">'+level+'</span>'+
            '<span>'+escapeHtml(description)+'</span>'+
          '</div>'
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
      const node=document.createElement("p");
      node.textContent=message;
      p("printStrengths").appendChild(node);
    });

    const weakest=[...rows].sort((a,b)=>a.level-b.level||a.index-b.index)[0];
    p("printTipText").textContent=NEXT_STEPS[weakest.criterion.id];

    p("printWarning").classList.toggle("hidden",assessment.grade<=4);
    const comment=(child.teacherComment||"").trim();
    p("printCustom").classList.toggle("hidden",!comment);
    p("printCustom").textContent=comment?"Persönliche Rückmeldung: "+comment:"";

    p("printFrontPoints").textContent=String(assessment.total);
    p("printFrontPercent").textContent=String(assessment.percent);
    p("printFrontGrade").textContent=gradeNames[assessment.grade]||String(assessment.grade);

    renderRubric();
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
