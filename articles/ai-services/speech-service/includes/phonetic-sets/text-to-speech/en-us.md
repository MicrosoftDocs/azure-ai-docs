---
author: PatrickFarley
ms.service: azure-speech-foundry-tools
ms.topic: include
ms.author: pafarley
---

#### Suprasegmentals for English

|Example&nbsp;1 (onset for consonant, word-initial for vowel)|Example&nbsp;2 (intervocalic for consonant, word-medial nucleus for vowel)|Example&nbsp;3 (coda for consonant, word-final for vowel)|Comments|
|--|--|--|--|
| :::no-loc text="burger":::  /b er **1** r - g ax r/ | :::no-loc text="falafel":::  /f ax - l aa **1** - f ax  l/ | :::no-loc text="guitar":::  /g ih - t aa **1** r/ | The Speech service phone set puts stress after the vowel of the stressed syllable. |
| :::no-loc text="inopportune"::: /ih **2** - n aa - p ax r - t uw 1 n/ | :::no-loc text="dissimilarity":::  /d ih - s ih **2**- m ax -  l eh 1 - r ax - t iy/ | :::no-loc text="workforce"::: /w er 1 r k - f ao **2** r s/ | The Speech service phone set puts stress after the vowel of the sub-stressed syllable. |

#### Vowels for English

| `sapi` | `ipa` | VisemeID | Example&nbsp;1     | Example&nbsp;2 | Example&nbsp;3                   |
|--------|-------|----------|---------------|-----------|-----------------------------|
| iy     | `i`   | 6        | **ea**t       | f**ee**l  | vall**ey**                  |
| ih     | `ɪ`   | 6        | **i**f        | f**i**ll  |                             |
| ey     | `eɪ`  | 4,6      | **a**te       | g**a**te  | d**ay**                     |
| eh     | `ɛ`   | 4        | **e**very     | p**e**t   | m**eh** (rare word-final) |
| ae     | `æ`   | 1        | **a**ctive    | c**a**t   | n**ah** (rare word-final) |
| aa     | `ɑ`   | 2        | **o**bstinate | p**o**ppy | r**ah** (rare word-final) |
| ao     | `ɔ`   | 3        | **o**range    | c**au**se | Ut**ah**                    |
| uh     | `ʊ`   | 4        | b**oo**k      |           |                             |
| ow     | `oʊ`  | 8,4      | **o**ld       | cl**o**ne | g**o**                      |
| uw     | `u`   | 7        | **U**ber      | b**oo**st | t**oo**                     |
| ah     | `ʌ`   | 1        | **u**ncle     | c**u**t   |                             |
| ay     | `aɪ`  | 11       | **i**ce       | b**i**te  | fl**y**                     |
| aw     | `aʊ`  | 9        | **ou**t       | s**ou**th | c**ow**                     |
| oy     | `ɔɪ`  | 10       | **oi**l       | j**oi**n  | t**oy**                     |
| y uw   | `ju`  | 6,7      | **Yu**ma      | h**u**man | f**ew**                     |
| ax     | `ə`   | 1        | **a**go       | wom**a**n | are**a**                    |

#### R-colored vowels for English

| `sapi` | `ipa` | VisemeID | Example&nbsp;1    | Example&nbsp;2      | Example&nbsp;3  |
|--------|-------|----------|--------------|----------------|------------|
| ih r   | `ɪɹ`  | 6,13     | **ear**s     | t**ir**amisu   | n**ear**   |
| eh r   | `ɛɹ`  | 4,13     | **air**plane | app**ar**ently | sc**ar**e  |
| uh r   | `ʊɹ`  | 4,13     |              |                | c**ur**e   |
| ay r   | `aɪɹ` | 11,13    | **Ire**land  | f**ir**eplace  | ch**oir**  |
| aw r   | `aʊɹ` | 9,13     | **hour**s    | p**ower**ful   | s**our**   |
| ao r   | `ɔɹ`  | 3,13     | **or**ange   | m**or**al      | s**oar**   |
| aa r   | `ɑɹ`  | 2,13     | **ar**tist   | st**ar**t      | c**ar**    |
| er r   | `ɝ`   | 5        | **ear**th    | b**ir**d       | f**ur**    |
| ax r   | `ɚ`   | 1        |              | all**er**gy    | supp**er** |

#### Semivowels for English

| `sapi` | `ipa` | VisemeID | Example&nbsp;1           | Example&nbsp;2  | Example&nbsp;3 |
|--------|-------|----------|---------------------|------------|-----------|
| w      | `w`   | 7        | **w**ith, s**ue**de | al**w**ays |           |
| y      | `j`   | 6        | **y**ard, f**e**w   | on**i**on  |           |

#### Aspirated oral stops for English

| `sapi` | `ipa` | VisemeID | Example&nbsp;1 | Example&nbsp;2   | Example&nbsp;3  |
|--------|-------|----------|-----------|-------------|------------|
| p      | `p`   | 21       | **p**ut   | ha**pp**en  | fla**p**   |
| b      | `b`   | 21       | **b**ig   | num**b**er  | cra**b**   |
| t      | `t`   | 19       | **t**alk  | capi**t**al | sough**t** |
| d      | `d`   | 19       | **d**ig   | ran**d**om  | ro**d**    |
| k      | `k`   | 20       | **c**ut   | sla**ck**er | Ira**q**   |
| g      | `g`   | 20       | **g**o    | a**g**o     | dra**g**   |

#### Nasal stops for English

| `sapi` | `ipa` | VisemeID | Example&nbsp;1        | Example&nbsp;2  | Example&nbsp;3   |
|--------|-------|----------|------------------|------------|-------------|
| m      | `m`   | 21       | **m**at, s**m**ash   | ca**m**era | roo**m**    |
| n      | `n`   | 19       | **n**o, s**n**ow | te**n**t   | chicke**n** |
| ng     | `ŋ`   | 20       |                  | li**n**k   | si**ng**    |

#### Fricatives for English

| `sapi` | `ipa` | VisemeID | Example&nbsp;1   | Example&nbsp;2        | Example&nbsp;3  |
|--------|-------|----------|-------------|------------------|------------|
| f      | `f`   | 18       | **f**ork    | le**f**t         | hal**f**   |
| v      | `v`   | 18       | **v**alue   | e**v**ent        | lo**v**e   |
| th     | `θ`   | 19       | **th**in    | empa**th**y      | mon**th**  |
| dh     | `ð`   | 17       | **th**en    | mo**th**er       | smoo**th** |
| s      | `s`   | 15       | **s**it     | ri**s**k         | fact**s**  |
| z      | `z`   | 15       | **z**ap     | bu**s**y         | kid**s**   |
| sh     | `ʃ`   | 16       | **sh**e    | abbrevia**ti**on | ru**sh**   |
| zh     | `ʒ`   | 16       | **J**acques | plea**s**ure     | gara**g**e |
| h      | `h`   | 12       | **h**elp    | en**h**ance      | a-**h**a!  |

#### Affricates for English

| `sapi` | `ipa` | VisemeID | Example&nbsp;1 | Example&nbsp;2    | Example&nbsp;3  |
|--------|-------|----------|-----------|--------------|------------|
| ch     | `tʃ`  | 19,16    | **ch**in  | fu**t**ure   | atta**ch** |
| jh     | `dʒ`  | 19,16    | **j**oy   | ori**g**inal | oran**g**e |

#### Approximants for English

| `sapi` | `ipa` | VisemeID | Example&nbsp;1          | Example&nbsp;2  | Example&nbsp;3 |
|--------|-------|----------|--------------------|------------|-----------|
| l      | `l`   | 14       | **l**id, g**l**ad  | pa**l**ace | chi**ll** |
| r      | `ɹ`   | 13       | **r**ed, b**r**ing | bo**rr**ow | ta**r**   |

> [!NOTE]
> `en-CA` locale doesn't support SAPI phones.
