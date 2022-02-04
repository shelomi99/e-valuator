import spacy

nlp = spacy.load('en_core_web_md')
model_answer = "Three main steps. Glycolysis. Pyruvate oxidation and citric acid cycle /Krebs cycle / TCA cycle. Oxidative phosphorylation /Electron transport chain. Glycolysis takes place in the cytosol (of a cell). Does not depend on oxygen/oxygen is not involved.(one) Glucose (6C) molecule is oxidized (broken down) into two (3C) pyruvate molecules. Two ATP (molecules) are utilized (to initiate the process) and four Ht and electrons are produced. Electrons/ H* are accepted by two NAD+ (molecules) and two NADH (molecules) are produced. (In later steps of glycolysis) four ATP (molecules) are produced by substrate level phosphorylation. The net gain of ATP (molecules) in glycolysis is 2 ATP (as two ATP molecules are used up). Two pyruvate (molecules) enter mitochondria by active transport. Pyruvate is converted to acetyl group by releasing 2CO2 (molecules), in the matrix of mitochondria. Acetyl group combines with co-enzyme A to produce Acetyl Co-enzyme A.(In this reaction) two NAD+ (molecules) are converted to two NADH (molecules). Cytric acid cycle/ Krebs cycle/ TCA cycle takes place in the matrix of mitochondria (using specific enzymes). Acetyl Co-enzyme A is combined with (4C) oxaloacetic acid/oxaloacetate and produce (6C) citric acid/citrate. Citric acid/citrate undergoes a series of reactions to regenerate oxaloacetic acid/oxaloacetate by releasing two (molecules of) CO2 (decarboxylation) and one ATP molecule by substrate level phosphorylation. One FADH2 (molecule) and three (molecules of) NADH are produced (for one cycle/for one molecule of acetyl co-A) . These numbers should be doubled when the yield of one glucose molecule is considered. Electron transport chain takes place in the inner membrane (cristae) of mitochondria and synthesize ATP by oxidation of reduced co-enzymes / NADH and FADH2 . This process is oxidative phosphorylation. Electrons (of reduced co-enzymes) pass through a series of proteins and non-protein molecules and are finally accepted by molecular oxygen/O2 /02 is the final electron acceptor. One (molecule of) NADH produces 2.5 molecules of ATP. One (molecule of) FADH2 produces 1.5 molecules of ATP. Total number of ATP molecules produced in the electron transport chain is Thus the total number of ATP molecules produced for one molecule of glucose is 32 (during aerobic respiration in the liver cell)"

doc = nlp(model_answer)

sentences = list(doc.sents)
for sentence in sentences:
    print(sentence)

for token in doc:
    print('{:<12}{:<10}{:<10}'.format(token.text, token.pos_, token.dep_))

for ent in doc.ents:
    print(ent.text, ent.label_)


