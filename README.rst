.. raw:: html

   <table>
   <tr>
   <td>
   <img src="https://img.shields.io/github/languages/top/AstraBert/resistML" alt="GitHub top language">
   </td>
   <td>
   <img src="https://img.shields.io/github/commit-activity/t/AstraBert/resistML" alt="GitHub commit activity">
   </td>
   <td>
   <img src="https://img.shields.io/badge/resistML-stable-green" alt="Static Badge">
   </td>
   <td>
   <img src="https://img.shields.io/badge/resistBERT-unstable-orange" alt="Static Badge">
   </td>
   <td>
   <img src="https://img.shields.io/badge/Release-v0.0.0-blue" alt="Static Badge">
   </td>
   </tr>
   </table>

========
resistML
========

A tool for AMR gene family prediction, simple and ML-based.

Training
========

Data collection for training
----------------------------

Latest reference sequences release (Feb 2024) were downloaded from **CARD** (*The Comprehensive Antibiotic Resistance Database*). If you want to automatically download them too, use `this link <https://card.mcmaster.ca/latest/data>`_.

Protein sequences were mapped with their ARO indices to the corrresponding AMR gene families (see `this file <https://github.com/AstraBert/resistML/tree/main/data/aro_categories_index.tsv>`_ for reference) and the 12 most common families were chosen to train resistML and resistBERT.

Training procedures
-------------------

resistML (stable)
~~~~~~~~~~~~~~~~~

resistML was trained starting from all the protein sequences retrieved beforehands, extracting their features in a `csv file <https://github.com/AstraBert/resistML/tree/main/data/proteinstats.tsv>`_. 

Features were extracted through biopython ::menuselection:`Bio.SeqUtils.ProtParam --> ProteinAnalysis` subclass, and they are (maiusc is for the header you can find in the csv):

- HIDROPHOBICITY score
- ISOELECTRIC point
- AROMATICity
- INSTABility
- MW (molar weight)
- HELIX,TURN,SHEET (percentage of these three secondary strcutures)
- MOL_EXT_RED,MOL_EXT_OX (molar extinction reduced and oxidized)

Dataset building occured `here <https://github.com/AstraBert/resistML/tree/main/scripts/build_base_dataset.py>`_ 

The base model itself is a simple Voting Classifier based on a DecisionTreeClassifier, ExtraTreesClassifier and HistGradientBoostingClassifier, all provided by scikit-learn library.

During validation, it yielded 100% accuracy on predicting training data.

resistBERT (unstable)
~~~~~~~~~~~~~~~~~~~~~

resistBERT is a BERT model for text classification, finetuned from `prot_bert <https://huggingface.co/Rostlab/prot_bert>`_ by RosettaLab.

Data using from finetuning were a selection of 1496 sequences out of the total 1836 ones. 80% were used for training, 20% were used for validations.

Sequences were preprocessed and labelled `here <https://github.com/AstraBert/resistML/tree/main/scripts/build_base_dataset.py>`_, then the complete jsonl file was reduced `here <https://github.com/AstraBert/resistML/tree/main/scripts/reduce_dataset.py>`_ and uploaded to Huggingface under the identifier :command:`as-cle-bert/AMR-Gene-Families` through `this script <https://github.com/AstraBert/resistML/tree/main/scripts/jsonl2hfdataset.py>`_.

Finetuning occurred from the HF dataset thanks to AutoTrain: during validation, the model yielded the following stats:

- loss: 0.08235077559947968

- f1_macro: 0.986759581881533

- f1_micro: 0.99

- f1_weighted: 0.9899790940766551

- precision_macro: 0.9871615312791784

- precision_micro: 0.99

- precision_weighted: 0.9901213818860879

- recall_macro: 0.986574074074074

- recall_micro: 0.99

- recall_weighted: 0.99

- accuracy: 0.99

The model is now available on Huggingface under the identifier :command:`as-cle-bert/resistBERT`. There is also a widget through which you can make inferences thanks to HF :command:`Inference API`. Keep in mind that Inference API *can* be unstable, so downloading the model and using it from a local machine/cloud service would be preferable. 

Testing
=======

Data retrieval for tests
------------------------

Data were downloaded from **CARD** (*The Comprehensive Antibiotic Resistance Database*), as the annotations for the family names used to label training sequences were the same. 

For families "PDC beta-lactamase", "CTX-M beta-lactamase", "SHV beta-lactamase", "CMY beta-lactamase", sequences were downloaded after having searched the exact AMR gene family as in the labels used for training, through `Download sequences` method. In the downloading customization page, filters were set to `is_a` and `Protein`.

For all the other families, procedure was the same but customization filters were set to `is_a`, `structurally_homologous_to`, `evolutionary_variant_of` and `Protein` to increase the number of retrieved sequences.

Test building
-------------

Test were built thanks to `this script <https://github.com/AstraBert/resistML/tree/main/scripts/build_tests.py>`_. 

These are the test metadata:

**Metadata for test 0:**

- Protein statistics for resistML were saved in test/testfiles/test_0.csv
- Sequences and labels for resistBERT were saved in test/testfiles/test_0.jsonl
- 12 protein sequences were taken into account for 2 families
- Families taken into account were: quinolone resistance protein (qnr), CMY beta-lactamase

**Metadata for test 1:**

- Protein statistics for resistML were saved in test/testfiles/test_1.csv
- Sequences and labels for resistBERT were saved in test/testfiles/test_1.jsonl
- 11 protein sequences were taken into account for 2 families
- Families taken into account were: VIM beta-lactamase,IMP beta-lactamase

**Metadata for test 2:**

- Protein statistics for resistML were saved in test/testfiles/test_2.csv
- Sequences and labels for resistBERT were saved in test/testfiles/test_2.jsonl
- 13 protein sequences were taken into account for 2 families
- Families taken into account were: quinolone resistance protein (qnr),SHV beta-lactamase

**Metadata for test 3:**

- Protein statistics for resistML were saved in test/testfiles/test_3.csv
- Sequences and labels for resistBERT were saved in test/testfiles/test_3.jsonl
- 10 protein sequences were taken into account for 3 families
- Families taken into account were: quinolone resistance protein (qnr),VIM beta-lactamase,CMY beta-lactamase

**Metadata for test 4:**

- Protein statistics for resistML were saved in test/testfiles/test_4.csv
- Sequences and labels for resistBERT were saved in test/testfiles/test_4.jsonl
- 12 protein sequences were taken into account for 2 families
- Families taken into account were: CMY beta-lactamase,IMP beta-lactamase

**Metadata for test 5:**

- Protein statistics for resistML were saved in test/testfiles/test_5.csv
- Sequences and labels for resistBERT were saved in test/testfiles/test_5.jsonl
- 12 protein sequences were taken into account for 2 families
- Families taken into account were: VIM beta-lactamase,SHV beta-lactamase

**Metadata for test 6:**

- Protein statistics for resistML were saved in test/testfiles/test_6.csv
- Sequences and labels for resistBERT were saved in test/testfiles/test_6.jsonl
- 11 protein sequences were taken into account for 3 families
- Families taken into account were: PDC beta-lactamase,MCR phosphoethanolamine transferase,ACT beta-lactamase

**Metadata for test 7:**

- Protein statistics for resistML were saved in test/testfiles/test_7.csv
- Sequences and labels for resistBERT were saved in test/testfiles/test_7.jsonl
- 10 protein sequences were taken into account for 3 families
- Families taken into account were: MCR phosphoethanolamine transferase,CTX-M beta-lactamase,PDC beta-lactamase

**Metadata for test 8:**

- Protein statistics for resistML were saved in test/testfiles/test_8.csv
- Sequences and labels for resistBERT were saved in test/testfiles/test_8.jsonl
- 12 protein sequences were taken into account for 2 families
- Families taken into account were: ACT beta-lactamase,CMY beta-lactamase

**Metadata for test 9:**
- Protein statistics for resistML were saved in test/testfiles/test_9.csv
- Sequences and labels for resistBERT were saved in test/testfiles/test_9.jsonl
- 15 protein sequences were taken into account for 3 families
- Families taken into account were: quinolone resistance protein (qnr),SHV beta-lactamase,KPC beta-lactamase

All data can be found `here <http://github.com/AstraBert/resistML/tree/main/test>`_ , along with the seqences use to generate them.

Test results
------------

**resistML** yielded 100% accuracy, f1 score, recall score and precision score in all 10 tests.

**resistBERT** was more unstable:

- On test_0, test_2, test_4, test_6, test_7, test_8 and test_9 yielded 100% accuracy, f1 score, recall score and precision score
- On test_1 it yielded:
  1. Accuracy: 50%
  2. f1 score: 33%
  3. Precision: 25%
  4. Recall: 50%
- On test_3 it yielded 66.7% accuracy, f1 score, recall score and precision score
- On test_5 it yielded 50% accuracy, f1 score, recall score and precision score


All results for resistBERT can be found `in the dedicated notebook <http://github.com/AstraBert/resistML/scripts/test_resistBERT.ipynb>`_ . 

License and rights of usage 
===========================

This repository is hereby provided under MIT license (more at `LICENSE <https://github.com/AstraBert/breastcancer-auto-class/blob/main/LICENSE>_`).

If you use this work for your projects, please consider citing the author `Astra Bertelli <http://astrabert.vercel.app>`_ .

References
==========

1. **CARD - The Comprehensive Antibiotic Resistance Database**

2. **Biopython**

3. **Scikit-learn** 

4. **Hugging Face's prot_bert Model**

5. **Hugging Face's AutoTrain**

If you feel that your work was relevant in building resistML and you weren't referenced in this section, feel free to flag an issue or to contact the author.