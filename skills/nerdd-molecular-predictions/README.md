# nerdd-molecular-predictions

## Example dialog

This is an example conversation that was held with Google Antigravity CLI:

```text
> Identify the five most likely metabolites of omeprazole. For each metabolite, estimate the 
  likelihood that it is a natural product and check whether it could activate CYP3A4. Present the 
  results in a table.

● Read(~/.gemini/config/skills/nerdd-molecular-predictions/SKILL.md)
● Find(Find files in nerdd-molecular-predictions skill)
● Bash(python3 /home/<user>/.gemini/config/skills/nerdd-molecular-predictions/scripts/list_modules.py)
● Bash(python3 /home/<user>/.gemini/config/skills/nerdd-molecular-predictions/scripts/get_module.py glory)
● Bash(python3 /home/<user>/.gemini/config/skills/nerdd-molecular-predictions/scripts/get_module.py np-scout)
● Bash(python3 /home/<user>/.gemini/config/skills/nerdd-molecular-predictions/scripts/get_module.py cypstrate)
● Bash(python3 /home/<user>/.gemini/config/skills/nerdd-molecular-predictions/scripts/create_job.py --module glory --input
'CC1=CN=C(C(=C1OC)C)CS(=O)C2=NC3=C(N2)C=CC(=C3)O...)
...
(many other tool calls)
...
▸ Thought for 3s
  Analyzing the Prompt's Details
  The five most likely metabolites of omeprazole were identified using the GLORY metabolite structure prediction engine (NERDD). Each metabolite's natural product-       
  likeness was evaluated using NP-Scout, and its interaction with CYP3A4 (substrate and inhibition potential) was evaluated using CYPstrate and CYPlebrity.               
  ──────                                                   
  ### Results Summary Table

Metabolite Name            │ Metabolic Reaction (GLORY Rank / Sco… │ SMILES                                 │ Natural Produc… │ CYP3A4 Interaction & Activation Poten…
───────────────────────────┼───────────────────────────────────────┼────────────────────────────────────────┼─────────────────┼────────────────────────────────────────
5-O-Desmethyl omeprazole   │ Oxidative ether cleavage / O-         │ COc1c(C)cnc(CS(=O)c2nc3cc(O)ccc3[nH]2) │ 25% (Low)       │ Substrate (CYP3A4 Substrate: Yes;
                           │ demethylation (Rank 1 / Score 4.77)   │ c1C                                    │                 │ Inhibition Probability: 0.45)
Omeprazole sulfone         │ S-Oxidation (Rank 3 / Score 3.97)     │ COc1ccc2[nH]c(S(=O)(=O)Cc3ncc(C)c(OC)c │ 5% (Very Low)   │ High Interaction / Substrate (CYP3A4
                           │                                       │ 3C)nc2c1                               │                 │ Substrate: Yes; Inhibition
                           │                                       │                                        │                 │ Probability: 0.85)
5-Hydroxymethyl omeprazole │ Aliphatic hydroxylation (Rank 4 /     │ COc1ccc2[nH]c(S(=O)Cc3ncc(CO)c(OC)c3C) │ 33% (Moderate-  │ Substrate (CYP3A4 Substrate: Yes;
                           │ Score 3.39)                           │ nc2c1                                  │ Low)            │ Inhibition Probability: 0.52)
4-O-Desmethyl omeprazole   │ Oxidative ether cleavage / O-         │ COc1ccc2[nH]c(S(=O)Cc3ncc(C)c(O)c3C)nc │ 14% (Low)       │ Low Potential (CYP3A4 Substrate:
                           │ demethylation (Rank 5 / Score 1.47)   │ 2c1                                    │                 │ Unpredicted; Inhibition Probability:
                           │                                       │                                        │                 │ 0.47)
3-Hydroxymethyl omeprazole │ Aliphatic hydroxylation (Rank 9 /     │ COc1ccc2[nH]c(S(=O)Cc3ncc(C)c(OC)c3CO) │ 39% (Moderate-  │ Substrate (CYP3A4 Substrate: Yes;
                           │ Score 0.42)                           │ nc2c1                                  │ Low)            │ Inhibition Probability: 0.51)
  
  (For baseline comparison, parent Omeprazole has an NP-Scout probability of 14%, is classified as a CYP3A4 Substrate, and has a 0.56 CYP3A4 inhibition probability).     
  ──────
  ### Key Takeaways
  
  1. Metabolite Ranking:
      • The primary metabolic pathways of omeprazole are O-demethylation (forming 5-O-desmethyl omeprazole), S-oxidation (forming omeprazole sulfone via CYP3A4), and     
      aliphatic hydroxylation of the pyridine methyl group (forming 5-hydroxymethyl omeprazole via CYP2C19).
  2. Natural Product-Likeness:
      • All predicted metabolites exhibit overall low NP-likeness (ranging from 5% to 39%), reflecting their synthetic benzimidazole/pyridine drug core structure.        
      • Hydroxylated metabolites (e.g., 3-hydroxymethyl and 5-hydroxymethyl derivatives) show slightly higher natural product probabilities (33%–39%) due to the          
      introduction of primary alcohol functional groups commonly found in natural secondary metabolites.
  3. CYP3A4 Activation & Interaction:
      • Omeprazole sulfone shows the strongest affinity for CYP3A4 (CYP3A4 substrate with an 85% inhibition probability), consistent with known clinical 
      pharmacokinetics where CYP3A4 is the main enzyme generating omeprazole sulfone.
      • Most hydroxylated and demethylated metabolites remain active substrates for CYP3A4 with moderate inhibition probabilities (~0.45–0.52), indicating they are       
      processed by CYP3A4 but are not strong classical transcriptional activators/inducers of the enzyme. 
```

(Note: result table indentation was changed for better rendering in GitHub markdown)