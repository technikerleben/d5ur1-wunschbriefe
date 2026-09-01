from pathlib import Path

src = Path('tools/generate_offener_anfang.py').read_text(encoding='utf-8')
repl = {
    'waehlen':'wählen','Waehle':'Wähle','WAEHLEN':'WÄHLEN',
    'moechtest':'möchtest','moechte':'möchte','moechten':'möchten','moechtest':'möchtest',
    'koennten':'könnten','Koennten':'Könnten','koennen':'können','koennte':'könnte','koenntest':'könntest',
    'pruefe':'prüfe','Pruefe':'Prüfe','pruefen':'prüfen','pruefst':'prüfst',
    'wuensche':'wünsche','Wuensche':'Wünsche','gewuenscht':'gewünscht',
    'Baelle':'Bälle','baelle':'bälle','Gruesse':'Grüße','GRUSS':'GRUß','Gruss':'Gruß',
    'gemuetliche':'gemütliche','gemuetlichen':'gemütlichen','gemuetlich':'gemütlich',
    'moeglich':'möglich','moegliche':'mögliche','moeglichen':'möglichen','moeglichst':'möglichst',
    'wuerde':'würde','wuerden':'würden','wuerdest':'würdest',
    'gaebe':'gäbe','haetten':'hätten','faende':'fände','geaendert':'geändert',
    'Erklaerung':'Erklärung','vollstaendig':'vollständig','Empfaenger':'Empfänger','EMPFAENGER':'EMPFÄNGER',
    'zusaetzliche':'zusätzliche','zusaetzlichen':'zusätzlichen','zusaetzlich':'zusätzlich',
    'Sitzplaetze':'Sitzplätze','sitzplaetze':'sitzplätze','Loesung':'Lösung','LOESUNG':'LÖSUNG',
    'fuer':'für','Fuer':'Für','uebertrieben':'übertrieben','naechsten':'nächsten',
    'tuefteln':'tüfteln','Tuefteln':'Tüfteln','zurueckziehen':'zurückziehen','ergaenze':'ergänze',
    'Ablagefaecher':'Ablagefächer','selbststaendig':'selbstständig','Einfuehrung':'Einführung',
    'Uebersicht':'Übersicht','ueben':'üben','Ueben':'Üben','unsicher':'unsicher',
    'Pausenraeume':'Pausenräume','Pausenraum':'Pausenraum','Sitzmoebel':'Sitzmöbel',
    'geaendert':'geändert','anzuschaffen':'anzuschaffen','zurueck':'zurück',
    'schon':'schon','waere':'wäre','Waere':'Wäre','waeren':'wären',
    'haette':'hätte','koennte':'könnte','moeglicherweise':'möglicherweise',
    'faellt':'fällt','klaeren':'klären','erklaeren':'erklären','ueber':'über',
    'Schueler':'Schüler','Schuelerinnen':'Schülerinnen','Lehrkraefte':'Lehrkräfte'
}
for a,b in sorted(repl.items(), key=lambda kv: -len(kv[0])):
    src = src.replace(a,b)
exec(compile(src, 'generate_offener_anfang_de.py', 'exec'), {'__name__':'__main__'})
