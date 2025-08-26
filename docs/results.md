# Results

## CDL

Running all registered solvers with all registered preprocessors on all files in the CDL directory using a timeout of 5s leads to the following results table:

| Solver     | Preprocessor                 | Avg. preprocessor time   | Avg. solver time    | Avg. total time     | Avg. speedup       |   Percentage finished |
| ---------- | ---------------------------- | ------------------------ | ------------------- | ------------------- | ------------------ | --------------------- |
| CountAntom | HiddenTautologyElimination   | 0.00633544346381878      | 0.17975132013189382 | 0.1860867635957126  | 1.270907353165504  |              1 |
| CountAntom | Subsumption                  | 0.005043401800352952     | 0.19411836821457434 | 0.1991617700149273  | 1.1874720543146218 |              1 |
| CountAntom | EquivalentLiteralElimination | 0.0053409831277255355    | 0.20974516868591309 | 0.21508615181363863 | 1.0995549187447295 |              1 |
| CountAntom | BinaryResolution             | 0.00488371930665021      | 0.23079785031953291 | 0.2356815696261831  | 1.0034685213429098 |              0.991379 |
| CountAntom | SharpSatPreprocessor         | 0.014949186094875994     | 0.21959049742797326 | 0.23453968352284926 | 1.0083540347129436 |              1 |
| CountAntom | NoPreprocessor               | 0.0020078749492250638    | 0.23449116123133693 | 0.23649903618056198 | 1.0                |              1 |
| CountAntom | Probing                      | 0.005004716330561145     | 0.23309006773192306 | 0.23809478406248422 | 0.9932978461153376 |              1 |
| CountAntom | UnitPropagation              | 0.004987303552956417     | 0.23595674695639773 | 0.24094405050935416 | 0.9815516742604955 |              1 |
| CountAntom | HyperBinaryResolution        | 0.005565089642401684     | 0.2428769422490104  | 0.2484420318914121  | 0.9519284413352805 |              0.991379 |
| SharpSat   | EquivalentLiteralElimination | 0.005213718989799763     | 0.4535044185046492  | 0.45871813749444895 | 1.8842080865110702 |              1 |
| Ganak      | EquivalentLiteralElimination | 0.005136942041331324     | 0.47391113125044726 | 0.47904807329177856 | 2.2021836021796815 |              1 |
| Ganak      | HiddenTautologyElimination   | 0.006256935925319277     | 0.7400005295358855  | 0.7462574654612047  | 1.413656627216372  |              1 |
| Ganak      | Subsumption                  | 0.00485466060967281      | 0.7804489629022007  | 0.7853036235118734  | 1.3433680681889462 |              1 |
| SharpSat   | Subsumption                  | 0.004872975678279482     | 0.7842989337855372  | 0.7891719094638167  | 1.0952245179172417 |              1 |
| SharpSat   | HiddenTautologyElimination   | 0.006157264627259353     | 0.7863199032586197  | 0.7924771678858791  | 1.0906565628914175 |              1 |
| SharpSat   | BinaryResolution             | 0.005012881878443751     | 0.8350441074093118  | 0.8400569892877555  | 1.0288830818837111 |              1 |
| SharpSat   | SharpSatPreprocessor         | 0.014938107852278084     | 0.8336852398411981  | 0.8486233476934762  | 1.018497106455444  |              1 |
| SharpSat   | NoPreprocessor               | 0.002021162674344819     | 0.8622992614219929  | 0.8643204240963377  | 1.0                |              1 |
| SharpSat   | Probing                      | 0.004860323050926472     | 0.8613492188782528  | 0.8662095419291792  | 0.9978190983342966 |              1 |
| SharpSat   | UnitPropagation              | 0.0048898602354115455    | 0.8655181691564363  | 0.8704080293918478  | 0.9930060326996714 |              1 |
| SharpSat   | HyperBinaryResolution        | 0.005639710131067517     | 0.9187850869528421  | 0.924424797083909   | 0.9349818685336329 |              1 |
| Ganak      | SharpSatPreprocessor         | 0.014975987631699135     | 0.9637855065279993  | 0.9787614941596985  | 1.0778435992362354 |              1 |
| Ganak      | HyperBinaryResolution        | 0.005313040894819601     | 0.9867170057610323  | 0.9920300466558519  | 1.0634272774450564 |              1 |
| Ganak      | BinaryResolution             | 0.004645187510554583     | 1.012321080446602   | 1.0169662679571567  | 1.0373518226696665 |              1 |
| Ganak      | NoPreprocessor               | 0.001989973002466662     | 1.0529618386564583  | 1.054951811658925   | 1.0                |              1 |
| Ganak      | UnitPropagation              | 0.004842118970279036     | 1.050188529080358   | 1.055030648050637   | 0.9999252757331194 |              1 |
| Ganak      | Probing                      | 0.004898155557698217     | 1.051392664169443   | 1.0562908197271412  | 0.9987323490432661 |              1 |
| DSharp     | EquivalentLiteralElimination | 0.005162956478359463     | 1.5287740810497388  | 1.5339370375280983  | 2.219013137559305  |              0.956897 |
| D4         | EquivalentLiteralElimination | 0.0050890281282622235    | 1.7386209060405862  | 1.7437099341688485  | 1.5968198881050286 |              1 |
| D4         | HiddenTautologyElimination   | 0.0060706902476190365    | 2.4750003953581876  | 2.4810710856058065  | 1.1222534969356828 |              0.887931 |
| D4         | BinaryResolution             | 0.005136425349899575     | 2.639910905992106   | 2.6450473313420058  | 1.0526808609335636 |              0.87069 |
| D4         | Subsumption                  | 0.004767641290888056     | 2.716878573099772   | 2.72164621439066    | 1.0230538735140176 |              0.956897 |
| D4         | Probing                      | 0.004745471595537545     | 2.766757382024633   | 2.7715028536201705  | 1.0046501299214332 |              0.87069 |
| D4         | NoPreprocessor               | 0.001985458766712862     | 2.7824052432004143  | 2.7843907019671272  | 1.0                |              0.87931 |
| D4         | UnitPropagation              | 0.004696574865602979     | 2.797041077239841   | 2.801737652105444   | 0.9938085030462146 |              0.87931 |
| D4         | SharpSatPreprocessor         | 0.014899287268380138     | 2.8050527372092846  | 2.8199520244776646  | 0.9873893874073534 |              0.922414 |
| D4         | HyperBinaryResolution        | 0.005689131091102101     | 2.926791079497238   | 2.93248021058834    | 0.9495002530327386 |              0.913793 |
| DSharp     | Subsumption                  | 0.004842417911418434     | 3.094777456765036   | 3.0996198746764545  | 1.0981431840312195 |              0.887931 |
| DSharp     | NoPreprocessor               | 0.002204289803138146     | 3.401622148660513   | 3.403826438463651   | 1.0                |              0.672414 |
| DSharp     | BinaryResolution             | 0.004957855610090598     | 3.441247041062347   | 3.4462048966724375  | 0.987702861704565  |              0.594828 |
| DSharp     | UnitPropagation              | 0.004743117274660052     | 3.495873808860779   | 3.500616926135439   | 0.9723504485883175 |              0.568966 |
| DSharp     | Probing                      | 0.004825795398038977     | 3.5382809042930603  | 3.543106699691099   | 0.9606897920292407 |              0.586207 |
| DSharp     | HyperBinaryResolution        | 0.005552761001791035     | 3.654330606167439   | 3.6598833671692304  | 0.9300368610096915 |              0.594828 |
| DSharp     | HiddenTautologyElimination   | 0.006037616729736328     | 3.953510284423828   | 3.9595479011535644  | 0.8596502740810357 |              0.474138 |
| DSharp     | SharpSatPreprocessor         | 0.01431987160130551      | 4.01333423037278    | 4.027654101974085   | 0.8451138931705492 |              0.327586 |
| BddMiniSat | BinaryResolution             | No run finished          | No run finished     | No run finished     | No data            |              0 |
| BddMiniSat | EquivalentLiteralElimination | No run finished          | No run finished     | No run finished     | No data            |              0 |
| BddMiniSat | HiddenTautologyElimination   | No run finished          | No run finished     | No run finished     | No data            |              0 |
| BddMiniSat | HyperBinaryResolution        | No run finished          | No run finished     | No run finished     | No data            |              0 |
| BddMiniSat | NoPreprocessor               | No run finished          | No run finished     | No run finished     | No data            |              0 |
| BddMiniSat | Probing                      | No run finished          | No run finished     | No run finished     | No data            |              0 |
| BddMiniSat | SharpSatPreprocessor         | No run finished          | No run finished     | No run finished     | No data            |              0 |
| BddMiniSat | Subsumption                  | No run finished          | No run finished     | No run finished     | No data            |              0 |
| BddMiniSat | UnitPropagation              | No run finished          | No run finished     | No run finished     | No data            |              0 |
| RelSat     | BinaryResolution             | No run finished          | No run finished     | No run finished     | No data            |              0 |
| RelSat     | EquivalentLiteralElimination | No run finished          | No run finished     | No run finished     | No data            |              0 |
| RelSat     | HiddenTautologyElimination   | No run finished          | No run finished     | No run finished     | No data            |              0 |
| RelSat     | HyperBinaryResolution        | No run finished          | No run finished     | No run finished     | No data            |              0 |
| RelSat     | NoPreprocessor               | No run finished          | No run finished     | No run finished     | No data            |              0 |
| RelSat     | Probing                      | No run finished          | No run finished     | No run finished     | No data            |              0 |
| RelSat     | SharpSatPreprocessor         | No run finished          | No run finished     | No run finished     | No data            |              0 |
| RelSat     | Subsumption                  | No run finished          | No run finished     | No run finished     | No data            |              0 |
| RelSat     | UnitPropagation              | No run finished          | No run finished     | No run finished     | No data            |              0 |

It is immediately apparent from the raw data that not all solvers are created equal. While countAntom, sharpSAT and ganak were able to solve all given problems with and without preprocessing, d4, dsharp, bddminisat and relsat were unable to solve some or even most problems in the given timeframe (5s per problem) on the given hardware (AMD Ryzen 5 5600X).

For most solvers the most promising preprocessing is Equivalent Literal Elimination, which resulted in speedups for every solver that solved at least one problem. For dsharp, ganak, sharpsat and d4 speedups of 2.2x, 2.2x, 1.9x and 1.6x were measured. Another promising preprocessing seems to be Hidden Tautology Elimination which resulted in speedups for ganak, d4, sharpsat and countAntom. Finally, Subsumption lead to a performance gain in some solvers (countAntom and ganak) while not impacting performance in other solvers.

Other preprocessings resulted only in small improvements or no improvements at all. The probable reason for Unit Propagation not leading to improvements is that Unit Propagation is used internally by most solvers anyway. The sharpSAT preprocessor doesn't result in large improvements, which isn't surprising given that it is mostly a combination of two other preprocessings (Unit Propagation and Probing) which themselves didn't result in large improvements. Binary Resolution and Hyper Binary Resolution add binary clauses to the clause set, which can improve the performance of local search solvers. Local search solvers can however not be used for #SAT and adding additional binary clauses affects the performance of DPLL-solvers negatively.

## automotive01

Running all registered solvers with all registered preprocessors on all files in the automotive01 directory using a timeout of 30s leads to the following results table:

| Solver     | Preprocessor                 | Avg. preprocessor time   | Avg. solver time     | Avg. total time      | Avg. speedup         | Percentage finished |
| ---------- | ---------------------------- | ------------------------ | -------------------- | -------------------- | ------------------   | ------------------- |
| SharpSat   | EquivalentLiteralElimination | 0.01638507843017578      | 0.043476104736328125 | 0.059861183166503906 | 2.344385763673151                      | 1 |
| Ganak      | EquivalentLiteralElimination | 0.013413667678833008     | 0.04860973358154297  | 0.06202340126037598  | 2.707809106459859                      | 1 |
| DSharp     | EquivalentLiteralElimination | 0.013594388961791992     | 0.08703804016113281  | 0.1006324291229248   | 4.7570335692269055                     | 1 |
| D4         | HiddenTautologyElimination   | 0.01110386848449707      | 0.10805940628051758  | 0.11916327476501465  | 1.226089270458397                      | 1 |
| SharpSat   | SharpSatPreprocessor         | 0.04462623596191406      | 0.0773162841796875   | 0.12194252014160156  | 1.1508512818106456                     | 1 |
| Ganak      | Subsumption                  | 0.013974189758300781     | 0.11421847343444824  | 0.12819266319274902  | 1.3101181188032265                     | 1 |
| SharpSat   | BinaryResolution             | 0.012152433395385742     | 0.1252131462097168   | 0.13736557960510254  | 1.0216366138855477                     | 1 |
| SharpSat   | Subsumption                  | 0.013602018356323242     | 0.12408328056335449  | 0.13768529891967773  | 1.0192642694123228                     | 1 |
| SharpSat   | Probing                      | 0.011966228485107422     | 0.12682747840881348  | 0.1387937068939209   | 1.0111244144479965                     | 1 |
| SharpSat   | UnitPropagation              | 0.010930061340332031     | 0.12816452980041504  | 0.13909459114074707  | 1.0089371877169375                     | 1 |
| SharpSat   | NoPreprocessor               | 0.013978004455566406     | 0.1263597011566162   | 0.14033770561218262  | 1.0                                    | 1 |
| Ganak      | SharpSatPreprocessor         | 0.04518842697143555      | 0.09597325325012207  | 0.14116168022155762  | 1.1897529873749102                     | 1 |
| D4         | UnitPropagation              | 0.013936996459960938     | 0.13045144081115723  | 0.14438843727111816  | 1.0118872077528571                     | 1 |
| D4         | NoPreprocessor               | 0.002137422561645508     | 0.1439673900604248   | 0.1461048126220703   | 1.0                                    | 1 |
| Ganak      | HiddenTautologyElimination   | 0.011691808700561523     | 0.13901352882385254  | 0.15070533752441406  | 1.1144099705111816                     | 1 |
| D4         | BinaryResolution             | 0.01080775260925293      | 0.14196228981018066  | 0.1527700424194336   | 0.9563708323189193                     | 1 |
| D4         | Probing                      | 0.012184381484985352     | 0.14261889457702637  | 0.15480327606201172  | 0.9438095648799                        | 1 |
| SharpSat   | HyperBinaryResolution        | 0.011996984481811523     | 0.14320874214172363  | 0.15520572662353516  | 0.9042044302436327                     | 1 |
| Ganak      | Probing                      | 0.011222362518310547     | 0.14635825157165527  | 0.15758061408996582  | 1.0657880204133199                     | 1 |
| SharpSat   | HiddenTautologyElimination   | 0.011211633682250977     | 0.1465299129486084   | 0.15774154663085938  | 0.8896686295373751                     | 1 |
| Ganak      | HyperBinaryResolution        | 0.012832880020141602     | 0.1475389003753662   | 0.1603717803955078   | 1.0472386746113866                     | 1 |
| D4         | SharpSatPreprocessor         | 0.04606032371520996      | 0.12055015563964844  | 0.1666104793548584   | 0.8769245079169737                     | 1 |
| Ganak      | NoPreprocessor               | 0.0035924911499023438    | 0.16435503959655762  | 0.16794753074645996  | 1.0                                    | 1 |
| Ganak      | UnitPropagation              | 0.011998414993286133     | 0.15735602378845215  | 0.16935443878173828  | 0.9916925234118515                     | 1 |
| Ganak      | BinaryResolution             | 0.011750459671020508     | 0.15998458862304688  | 0.17173504829406738  | 0.9779455761346867                     | 1 |
| D4         | EquivalentLiteralElimination | 0.015085458755493164     | 0.17614054679870605  | 0.19122600555419922  | 0.7640425903299005                     | 1 |
| D4         | HyperBinaryResolution        | 0.012182950973510742     | 0.18473005294799805  | 0.1969130039215088   | 0.7419764551472129                     | 1 |
| D4         | Subsumption                  | 0.012893438339233398     | 0.18920302391052246  | 0.20209646224975586  | 0.7229459189716559                     | 1 |
| CountAntom | EquivalentLiteralElimination | 0.01458430290222168      | 0.1881251335144043   | 0.20270943641662598  | 1.0218154018054044                     | 1 |
| CountAntom | HiddenTautologyElimination   | 0.01115107536315918      | 0.19427800178527832  | 0.2054290771484375   | 1.0082877609002452                     | 1 |
| CountAntom | NoPreprocessor               | 0.0025415420532226562    | 0.2045900821685791   | 0.20713162422180176  | 1.0                                    | 1 |
| CountAntom | BinaryResolution             | 0.011015892028808594     | 0.2022557258605957   | 0.2132716178894043   | 0.9712104511215996                     | 1 |
| CountAntom | Subsumption                  | 0.012550830841064453     | 0.2007741928100586   | 0.21332502365112305  | 0.9709673093042749                     | 1 |
| CountAntom | Probing                      | 0.010944366455078125     | 0.2108449935913086   | 0.22178936004638672  | 0.9339114562505644                     | 1 |
| CountAntom | UnitPropagation              | 0.010755538940429688     | 0.2263014316558838   | 0.23705697059631348  | 0.8737630608404598                     | 1 |
| CountAntom | SharpSatPreprocessor         | 0.043311119079589844     | 0.1978907585144043   | 0.24120187759399414  | 0.858747976126697                      | 1 |
| CountAntom | HyperBinaryResolution        | 0.013158798217773438     | 0.23041415214538574  | 0.24357295036315918  | 0.8503884520550224                     | 1 |
| DSharp     | HyperBinaryResolution        | 0.011842966079711914     | 0.25418639183044434  | 0.26602935791015625  | 1.799469980498437                      | 1 |
| DSharp     | BinaryResolution             | 0.011011600494384766     | 0.28996849060058594  | 0.3009800910949707   | 1.5905099960234537                     | 1 |
| DSharp     | UnitPropagation              | 0.010871171951293945     | 0.3021574020385742   | 0.31302857398986816  | 1.529291199806236                      | 1 |
| DSharp     | HiddenTautologyElimination   | 0.01118326187133789      | 0.3274500370025635   | 0.33863329887390137  | 1.4136585063622493                     | 1 |
| DSharp     | Subsumption                  | 0.012671947479248047     | 0.40181469917297363  | 0.4144866466522217   | 1.154951184452192                      | 1 |
| DSharp     | NoPreprocessor               | 0.0016565322875976562    | 0.47705531120300293  | 0.4787118434906006   | 1.0                                    | 1 |
| DSharp     | Probing                      | 0.010671138763427734     | 0.49315714836120605  | 0.5038282871246338   | 0.9501488021298414                     | 1 |
| DSharp     | SharpSatPreprocessor         | 0.043259382247924805     | 0.6762559413909912   | 0.719515323638916    | 0.6653254319442944                     | 1 |
| BddMiniSat | BinaryResolution             | No run finished          | No run finished      | No run finished      | No data                                | 0 |
| BddMiniSat | EquivalentLiteralElimination | No run finished          | No run finished      | No run finished      | No data                                | 0 |
| BddMiniSat | HiddenTautologyElimination   | No run finished          | No run finished      | No run finished      | No data                                | 0 |
| BddMiniSat | HyperBinaryResolution        | No run finished          | No run finished      | No run finished      | No data                                | 0 |
| BddMiniSat | NoPreprocessor               | No run finished          | No run finished      | No run finished      | No data                                | 0 |
| BddMiniSat | Probing                      | No run finished          | No run finished      | No run finished      | No data                                | 0 |
| BddMiniSat | SharpSatPreprocessor         | No run finished          | No run finished      | No run finished      | No data                                | 0 |
| BddMiniSat | Subsumption                  | No run finished          | No run finished      | No run finished      | No data                                | 0 |
| BddMiniSat | UnitPropagation              | No run finished          | No run finished      | No run finished      | No data                                | 0 |
| RelSat     | BinaryResolution             | No run finished          | No run finished      | No run finished      | No data                                | 0 |
| RelSat     | EquivalentLiteralElimination | No run finished          | No run finished      | No run finished      | No data                                | 0 |
| RelSat     | HiddenTautologyElimination   | No run finished          | No run finished      | No run finished      | No data                                | 0 |
| RelSat     | HyperBinaryResolution        | No run finished          | No run finished      | No run finished      | No data                                | 0 |
| RelSat     | NoPreprocessor               | No run finished          | No run finished      | No run finished      | No data                                | 0 |
| RelSat     | Probing                      | No run finished          | No run finished      | No run finished      | No data                                | 0 |
| RelSat     | SharpSatPreprocessor         | No run finished          | No run finished      | No run finished      | No data                                | 0 |
| RelSat     | Subsumption                  | No run finished          | No run finished      | No run finished      | No data                                | 0 |
| RelSat     | UnitPropagation              | No run finished          | No run finished      | No run finished      | No data                                | 0 |

Just like in the previous example, not all solvers are able to solve the given problem. Unlike in the previous example most preprocessors lead to worse performance. Equivalent Literal Elimination seems to be the most promising preprocessing again. Several other preprocessings including Hidden Tautology Elimination, Subsumption and the SharpSAT preprocessor offer small performance improvements.

## automotive02

Running all registered solvers with all registered preprocessors on all files in the automotive02 directory using a timeout of 30s leads to the following results table:

| Solver     | Preprocessor                 | Avg. preprocessor time   | Avg. solver time    | Avg. total time    | Avg. speedup           | Percentage finished |
| ---------- | ---------------------------- | ------------------------ | ------------------- | ------------------ | --------------------   | ------------------- |
| Ganak      | NoPreprocessor               | 0.004021406173706055     | 0.28327178955078125 | 0.2872931957244873 | 1.0                                      | 1 |
| SharpSat   | NoPreprocessor               | 0.00675654411315918      | 0.30344080924987793 | 0.3101973533630371 | 1.0                                      | 1 |
| Ganak      | UnitPropagation              | 0.2785768508911133       | 0.22938060760498047 | 0.5079574584960938 | 0.565585150723201                        | 1 |
| Ganak      | BinaryResolution             | 0.27446794509887695      | 0.23522520065307617 | 0.5096931457519531 | 0.5636591312222613                       | 1 |
| Ganak      | Probing                      | 0.27169227600097656      | 0.25055837631225586 | 0.5222506523132324 | 0.5501059586081212                       | 1 |
| Ganak      | HiddenTautologyElimination   | 0.31740736961364746      | 0.20627856254577637 | 0.5236859321594238 | 0.5485982686986285                       | 1 |
| Ganak      | HyperBinaryResolution        | 0.3070816993713379       | 0.22913694381713867 | 0.5362186431884766 | 0.5357762162392888                       | 1 |
| SharpSat   | Probing                      | 0.2742116451263428       | 0.2675304412841797  | 0.5417420864105225 | 0.5725923112570861                       | 1 |
| Ganak      | EquivalentLiteralElimination | 0.3497610092163086       | 0.19461750984191895 | 0.5443785190582275 | 0.5277452832295868                       | 1 |
| SharpSat   | HiddenTautologyElimination   | 0.3183586597442627       | 0.23798227310180664 | 0.5563409328460693 | 0.5575670152044407                       | 1 |
| SharpSat   | BinaryResolution             | 0.2765848636627197       | 0.2918543815612793  | 0.568439245223999  | 0.5457001007043432                       | 1 |
| SharpSat   | UnitPropagation              | 0.2777981758117676       | 0.29439234733581543 | 0.572190523147583  | 0.5421224938446404                       | 1 |
| SharpSat   | EquivalentLiteralElimination | 0.3578605651855469       | 0.23687958717346191 | 0.5947401523590088 | 0.5215678681398153                       | 1 |
| SharpSat   | HyperBinaryResolution        | 0.3104097843170166       | 0.29348063468933105 | 0.6038904190063477 | 0.5136649690078566                       | 1 |
| Ganak      | Subsumption                  | 0.5702707767486572       | 0.25066566467285156 | 0.8209364414215088 | 0.34995790322941334                      | 1 |
| SharpSat   | Subsumption                  | 0.5734152793884277       | 0.2811012268066406  | 0.8545165061950684 | 0.363009200072989                        | 1 |
| DSharp     | NoPreprocessor               | 0.005649566650390625     | 1.3101229667663574  | 1.315772533416748  | 1.0                                      | 1 |
| DSharp     | EquivalentLiteralElimination | 0.3522827625274658       | 0.9922525882720947  | 1.3445353507995605 | 0.9786076153626545                       | 1 |
| DSharp     | HiddenTautologyElimination   | 0.3199436664581299       | 1.0654394626617432  | 1.385383129119873  | 0.9497535416449395                       | 1 |
| DSharp     | UnitPropagation              | 0.2770392894744873       | 1.1306512355804443  | 1.4076905250549316 | 0.9347029833602122                       | 1 |
| DSharp     | BinaryResolution             | 0.27611875534057617      | 1.1399726867675781  | 1.4160914421081543 | 0.9291578878959539                       | 1 |
| DSharp     | Probing                      | 0.2762746810913086       | 1.153686285018921   | 1.4299609661102295 | 0.920145769430269                        | 1 |
| DSharp     | HyperBinaryResolution        | 0.31478357315063477      | 1.1438264846801758  | 1.4586100578308105 | 0.9020728510356736                       | 1 |
| DSharp     | Subsumption                  | 0.5907211303710938       | 1.1206588745117188  | 1.7113800048828125 | 0.768837154613622                        | 1 |
| CountAntom | NoPreprocessor               | 0.021276473999023438     | 1.721834659576416   | 1.7431111335754395 | 1.0                                      | 1 |
| CountAntom | HiddenTautologyElimination   | 0.3184170722961426       | 1.634937047958374   | 1.9533541202545166 | 0.8923682170585213                       | 1 |
| CountAntom | BinaryResolution             | 0.27588653564453125      | 1.718337059020996   | 1.9942235946655273 | 0.874080087227027                        | 1 |
| CountAntom | Probing                      | 0.2748911380767822       | 1.7209069728851318  | 1.995798110961914  | 0.8733905117964627                       | 1 |
| D4         | HyperBinaryResolution        | 0.36082887649536133      | 10.71224594116211   | 11.07307481765747  | 1.0026850491826236                       | 1 |
| D4         | NoPreprocessor               | 0.0737612247467041       | 11.029045343399048  | 11.102806568145752 | 1.0                                      | 1 |
| D4         | HiddenTautologyElimination   | 0.37665605545043945      | 10.821794033050537  | 11.198450088500977 | 0.9914592180525558                       | 1 |
| D4         | EquivalentLiteralElimination | 0.4080338478088379       | 10.833482265472412  | 11.24151611328125  | 0.9876609574956158                       | 1 |
| D4         | BinaryResolution             | 0.32515621185302734      | 10.974707126617432  | 11.299863338470459 | 0.9825611368542992                       | 1 |
| D4         | Probing                      | 0.32593464851379395      | 11.014191627502441  | 11.340126276016235 | 0.9790725692030078                       | 1 |
| D4         | UnitPropagation              | 0.32040905952453613      | 11.04666805267334   | 11.367077112197876 | 0.9767512315220824                       | 1 |
| D4         | Subsumption                  | 0.6208639144897461       | 10.939122438430786  | 11.559986352920532 | 0.9604515290228455                       | 1 |
| D4         | SharpSatPreprocessor         | 6.01711893081665         | 10.879446506500244  | 16.896565437316895 | 0.6571043452194526                       | 1 |
| CountAntom | HyperBinaryResolution        | 0.3176908493041992       | 1.6845123767852783  | 2.0022032260894775 | 0.870596506319654                        | 1 |
| CountAntom | UnitPropagation              | 0.2738184928894043       | 1.7290916442871094  | 2.0029101371765137 | 0.8702892362573437                       | 1 |
| CountAntom | EquivalentLiteralElimination | 0.3627181053161621       | 1.7088499069213867  | 2.071568012237549  | 0.8414452836103916                       | 1 |
| CountAntom | Subsumption                  | 0.5959868431091309       | 1.706559658050537   | 2.302546501159668  | 0.7570362347503204                       | 1 |
| Ganak      | SharpSatPreprocessor         | 5.959552526473999        | 0.24221086502075195 | 6.201763391494751  | 0.046324436710772965                     | 1 |
| SharpSat   | SharpSatPreprocessor         | 5.974031925201416        | 0.3092069625854492  | 6.283238887786865  | 0.049369021121572765                     | 1 |
| DSharp     | SharpSatPreprocessor         | 5.962676048278809        | 1.3718574047088623  | 7.334533452987671  | 0.1793941689475528                       | 1 |
| CountAntom | SharpSatPreprocessor         | 5.9438934326171875       | 1.7432355880737305  | 7.687129020690918  | 0.22675710644164118                      | 1 |
| BddMiniSat | BinaryResolution             | No run finished          | No run finished     | No run finished    | No data                                  | 0 |
| BddMiniSat | EquivalentLiteralElimination | No run finished          | No run finished     | No run finished    | No data                                  | 0 |
| BddMiniSat | HiddenTautologyElimination   | No run finished          | No run finished     | No run finished    | No data                                  | 0 |
| BddMiniSat | HyperBinaryResolution        | No run finished          | No run finished     | No run finished    | No data                                  | 0 |
| BddMiniSat | NoPreprocessor               | No run finished          | No run finished     | No run finished    | No data                                  | 0 |
| BddMiniSat | Probing                      | No run finished          | No run finished     | No run finished    | No data                                  | 0 |
| BddMiniSat | SharpSatPreprocessor         | No run finished          | No run finished     | No run finished    | No data                                  | 0 |
| BddMiniSat | Subsumption                  | No run finished          | No run finished     | No run finished    | No data                                  | 0 |
| BddMiniSat | UnitPropagation              | No run finished          | No run finished     | No run finished    | No data                                  | 0 |
| RelSat     | BinaryResolution             | No run finished          | No run finished     | No run finished    | No data                                  | 0 |
| RelSat     | EquivalentLiteralElimination | No run finished          | No run finished     | No run finished    | No data                                  | 0 |
| RelSat     | HiddenTautologyElimination   | No run finished          | No run finished     | No run finished    | No data                                  | 0 |
| RelSat     | HyperBinaryResolution        | No run finished          | No run finished     | No run finished    | No data                                  | 0 |
| RelSat     | NoPreprocessor               | No run finished          | No run finished     | No run finished    | No data                                  | 0 |
| RelSat     | Probing                      | No run finished          | No run finished     | No run finished    | No data                                  | 0 |
| RelSat     | SharpSatPreprocessor         | No run finished          | No run finished     | No run finished    | No data                                  | 0 |
| RelSat     | Subsumption                  | No run finished          | No run finished     | No run finished    | No data                                  | 0 |
| RelSat     | UnitPropagation              | No run finished          | No run finished     | No run finished    | No data                                  | 0 |

For this problem no preprocessing offers a performance improvement.

## berkeleydb

Running all registered solvers with all registered preprocessors on all files in the berkeleydb directory using a timeout of 30s leads to the following results table:

| Solver     | Preprocessor                 | Avg. preprocessor time   | Avg. solver time      | Avg. total time       | Avg. speedup         | Percentage finished |
| ---------- | ---------------------------- | ------------------------ | --------------------- | --------------------- | ------------------   | ------------------- |
| Ganak      | Probing                      | 0.0025272369384765625    | 0.0028858184814453125 | 0.005413055419921875  | 1.4295278365045807                     | 1 |
| Ganak      | HiddenTautologyElimination   | 0.0027523040771484375    | 0.0027391910552978516 | 0.005491495132446289  | 1.4091086701688882                     | 1 |
| Ganak      | HyperBinaryResolution        | 0.0026445388793945312    | 0.002894163131713867  | 0.0055387020111083984 | 1.3970987043175067                     | 1 |
| Ganak      | UnitPropagation              | 0.0028488636016845703    | 0.0027992725372314453 | 0.005648136138916016  | 1.37002954833263                       | 1 |
| Ganak      | EquivalentLiteralElimination | 0.0029783248901367188    | 0.0028378963470458984 | 0.005816221237182617  | 1.3304365648698504                     | 1 |
| Ganak      | Subsumption                  | 0.00312042236328125      | 0.0027587413787841797 | 0.00587916374206543   | 1.3161928707571273                     | 1 |
| SharpSat   | Subsumption                  | 0.0026900768280029297    | 0.0033502578735351562 | 0.006040334701538086  | 1.2335898954016182                     | 1 |
| SharpSat   | Probing                      | 0.0025663375854492188    | 0.0034978389739990234 | 0.006064176559448242  | 1.2287399252997837                     | 1 |
| SharpSat   | BinaryResolution             | 0.0026044845581054688    | 0.0034787654876708984 | 0.006083250045776367  | 1.2248873211836175                     | 1 |
| SharpSat   | HiddenTautologyElimination   | 0.003023862838745117     | 0.0032546520233154297 | 0.006278514862060547  | 1.1867927394243183                     | 1 |
| SharpSat   | HyperBinaryResolution        | 0.0026781558990478516    | 0.003620624542236328  | 0.00629878044128418   | 1.1829743745031984                     | 1 |
| SharpSat   | EquivalentLiteralElimination | 0.003208160400390625     | 0.0034513473510742188 | 0.006659507751464844  | 1.1188958900186166                     | 1 |
| SharpSat   | UnitPropagation              | 0.0027947425842285156    | 0.004181861877441406  | 0.006976604461669922  | 1.0680404620326704                     | 1 |
| Ganak      | SharpSatPreprocessor         | 0.003969907760620117     | 0.0030150413513183594 | 0.0069849491119384766 | 1.107826739939243                      | 1 |
| SharpSat   | NoPreprocessor               | 0.003370523452758789     | 0.004080772399902344  | 0.007451295852661133  | 1.0                                    | 1 |
| Ganak      | BinaryResolution             | 0.0032999515533447266    | 0.0043675899505615234 | 0.00766754150390625   | 1.0092039800995025                     | 1 |
| Ganak      | NoPreprocessor               | 0.004102230072021484     | 0.003635883331298828  | 0.0077381134033203125 | 1.0                                    | 1 |
| SharpSat   | SharpSatPreprocessor         | 0.0040204524993896484    | 0.0037550926208496094 | 0.007775545120239258  | 0.9582988378867323                     | 1 |
| DSharp     | HiddenTautologyElimination   | 0.0027289390563964844    | 0.006884098052978516  | 0.009613037109375     | 1.161483134920635                      | 1 |
| DSharp     | Probing                      | 0.0025064945220947266    | 0.007410287857055664  | 0.00991678237915039   | 1.1259075828244458                     | 1 |
| DSharp     | UnitPropagation              | 0.0027539730072021484    | 0.0071947574615478516 | 0.00994873046875      | 1.122291986196319                      | 1 |
| D4         | NoPreprocessor               | 0.0015540122985839844    | 0.008433818817138672  | 0.009987831115722656  | 1.0                                    | 1 |
| DSharp     | EquivalentLiteralElimination | 0.0030548572540283203    | 0.007082223892211914  | 0.010137081146240234  | 1.1014393903758408                     | 1 |
| RelSat     | EquivalentLiteralElimination | 0.0027399063110351562    | 0.00741887092590332   | 0.010158777236938477  | No data                                | 1 |
| DSharp     | HyperBinaryResolution        | 0.002887725830078125     | 0.007485389709472656  | 0.010373115539550781  | 1.0763767582973247                     | 1 |
| D4         | UnitPropagation              | 0.002684354782104492     | 0.008363008499145508  | 0.01104736328125      | 0.9040918508287292                     | 1 |
| DSharp     | SharpSatPreprocessor         | 0.0044400691986083984    | 0.0066831111907958984 | 0.011123180389404297  | 1.0037938869121619                     | 1 |
| DSharp     | NoPreprocessor               | 0.003755331039428711     | 0.0074100494384765625 | 0.011165380477905273  | 1.0                                    | 1 |
| D4         | HiddenTautologyElimination   | 0.003200531005859375     | 0.008475065231323242  | 0.011675596237182617  | 0.8554450593208225                     | 1 |
| D4         | Subsumption                  | 0.003055572509765625     | 0.008832454681396484  | 0.01188802719116211   | 0.8401588383939673                     | 1 |
| DSharp     | BinaryResolution             | 0.002562284469604492     | 0.009339570999145508  | 0.01190185546875      | 0.9381209935897435                     | 1 |
| D4         | Probing                      | 0.003209829330444336     | 0.009203195571899414  | 0.01241302490234375   | 0.8046250768285187                     | 1 |
| D4         | BinaryResolution             | 0.0038411617279052734    | 0.008826255798339844  | 0.012667417526245117  | 0.7884662438124636                     | 1 |
| D4         | HyperBinaryResolution        | 0.003773212432861328     | 0.008992195129394531  | 0.01276540756225586   | 0.7824138059840873                     | 1 |
| D4         | EquivalentLiteralElimination | 0.0052111148834228516    | 0.008403539657592773  | 0.013614654541015625  | 0.7336088540207341                     | 1 |
| DSharp     | Subsumption                  | 0.003486156463623047     | 0.010309457778930664  | 0.013795614242553711  | 0.8093427578936453                     | 1 |
| D4         | SharpSatPreprocessor         | 0.005515575408935547     | 0.009991168975830078  | 0.015506744384765625  | 0.6440959409594096                     | 1 |
| CountAntom | NoPreprocessor               | 0.0010251998901367188    | 0.05933213233947754   | 0.06035733222961426   | 1.0                                    | 1 |
| CountAntom | BinaryResolution             | 0.002780437469482422     | 0.05901813507080078   | 0.0617985725402832    | 0.9766784206911984                     | 1 |
| CountAntom | UnitPropagation              | 0.002390623092651367     | 0.059432029724121094  | 0.06182265281677246   | 0.9762979988661913                     | 1 |
| CountAntom | HiddenTautologyElimination   | 0.002445697784423828     | 0.05942893028259277   | 0.0618746280670166    | 0.9754778996690056                     | 1 |
| CountAntom | Probing                      | 0.0024900436401367188    | 0.060105323791503906  | 0.06259536743164062   | 0.9642459930525931                     | 1 |
| CountAntom | EquivalentLiteralElimination | 0.0036203861236572266    | 0.0593876838684082    | 0.06300806999206543   | 0.9579301863589065                     | 1 |
| CountAntom | Subsumption                  | 0.003955841064453125     | 0.05911874771118164   | 0.06307458877563477   | 0.9569199482903301                     | 1 |
| CountAntom | SharpSatPreprocessor         | 0.004526615142822266     | 0.05934405326843262   | 0.06387066841125488   | 0.944992963608605                      | 1 |
| CountAntom | HyperBinaryResolution        | 0.012044191360473633     | 0.06637287139892578   | 0.07841706275939941   | 0.7696964168984965                     | 1 |
| BddMiniSat | BinaryResolution             | No run finished          | No run finished       | No run finished       | No data                                | 0 |
| BddMiniSat | EquivalentLiteralElimination | No run finished          | No run finished       | No run finished       | No data                                | 0 |
| BddMiniSat | HiddenTautologyElimination   | No run finished          | No run finished       | No run finished       | No data                                | 0 |
| BddMiniSat | HyperBinaryResolution        | No run finished          | No run finished       | No run finished       | No data                                | 0 |
| BddMiniSat | NoPreprocessor               | No run finished          | No run finished       | No run finished       | No data                                | 0 |
| BddMiniSat | Probing                      | No run finished          | No run finished       | No run finished       | No data                                | 0 |
| BddMiniSat | SharpSatPreprocessor         | No run finished          | No run finished       | No run finished       | No data                                | 0 |
| BddMiniSat | Subsumption                  | No run finished          | No run finished       | No run finished       | No data                                | 0 |
| BddMiniSat | UnitPropagation              | No run finished          | No run finished       | No run finished       | No data                                | 0 |
| RelSat     | BinaryResolution             | No run finished          | No run finished       | No run finished       | No data                                | 0 |
| RelSat     | HiddenTautologyElimination   | No run finished          | No run finished       | No run finished       | No data                                | 0 |
| RelSat     | HyperBinaryResolution        | No run finished          | No run finished       | No run finished       | No data                                | 0 |
| RelSat     | NoPreprocessor               | No run finished          | No run finished       | No run finished       | No data                                | 0 |
| RelSat     | Probing                      | No run finished          | No run finished       | No run finished       | No data                                | 0 |
| RelSat     | SharpSatPreprocessor         | No run finished          | No run finished       | No run finished       | No data                                | 0 |
| RelSat     | Subsumption                  | No run finished          | No run finished       | No run finished       | No data                                | 0 |
| RelSat     | UnitPropagation              | No run finished          | No run finished       | No run finished       | No data                                | 0 |

For ganak and sharpsat almost all preprocessings offer a performance improvement. For dsharp some preprocessings including Hidden Tautology Elimination, Probing, Unit Propagation and Equivalent Literal Elimination offer a performance improvement while other preprocessings such as Subsumption lead to performance deterioration. For all other solvers preprocessings offer no performance improvements.

## busybox

Running all registered solvers with all registered preprocessors on all files in the busybox directory using a timeout of 30s leads to the following results table:

| Solver     | Preprocessor                   | Avg. preprocessor time   | Avg. solver time   | Avg. total time   | Avg. speedup   | Percentage finished |
| ---------- | ----------------------------   | ------------------------ | ------------------ | ----------------- | -------------- | --------------------- |
| RelSat     | NoPreprocessor                            | 0.000980616         | 0.00154948        | 0.0025301        | 1                            | 1 |
| RelSat     | SharpSatPreprocessor                      | 0.00138497          | 0.0014782         | 0.00286317       | 0.883671                     | 1 |
| RelSat     | HyperBinaryResolution                     | 0.00137925          | 0.00163913        | 0.00301838       | 0.838231                     | 1 |
| RelSat     | UnitPropagation                           | 0.00159311          | 0.00146985        | 0.00306296       | 0.826029                     | 1 |
| RelSat     | BinaryResolution                          | 0.00158691          | 0.00150633        | 0.00309324       | 0.817944                     | 1 |
| RelSat     | Probing                                   | 0.00143719          | 0.00169134        | 0.00312853       | 0.808718                     | 1 |
| RelSat     | HiddenTautologyElimination                | 0.0016253           | 0.00150919        | 0.00313449       | 0.80718                      | 1 |
| RelSat     | EquivalentLiteralElimination              | 0.00153494          | 0.00160742        | 0.00314236       | 0.805159                     | 1 |
| RelSat     | Subsumption                               | 0.00160789          | 0.00154305        | 0.00315094       | 0.802966                     | 1 |
| Ganak      | HyperBinaryResolution                     | 0.00142813          | 0.00180173        | 0.00322986       | 1.92212                      | 1 |
| Ganak      | BinaryResolution                          | 0.00152564          | 0.00171638        | 0.00324202       | 1.91491                      | 1 |
| Ganak      | UnitPropagation                           | 0.00150466          | 0.00175977        | 0.00326443       | 1.90177                      | 1 |
| Ganak      | HiddenTautologyElimination                | 0.00154519          | 0.00173473        | 0.00327992       | 1.89278                      | 1 |
| Ganak      | Subsumption                               | 0.00152612          | 0.00176382        | 0.00328994       | 1.88702                      | 1 |
| Ganak      | SharpSatPreprocessor                      | 0.00132394          | 0.00197196        | 0.0032959        | 1.88361                      | 1 |
| SharpSat   | Subsumption                               | 0.00136065          | 0.00194359        | 0.00330424       | 1.31965                      | 1 |
| SharpSat   | SharpSatPreprocessor                      | 0.00137997          | 0.00193596        | 0.00331593       | 1.315                        | 1 |
| SharpSat   | UnitPropagation                           | 0.00137186          | 0.00195813        | 0.00332999       | 1.30944                      | 1 |
| Ganak      | EquivalentLiteralElimination              | 0.00156164          | 0.00181913        | 0.00338078       | 1.83632                      | 1 |
| Ganak      | Probing                                   | 0.00159025          | 0.00180912        | 0.00339937       | 1.82627                      | 1 |
| SharpSat   | Probing                                   | 0.00138426          | 0.00205421        | 0.00343847       | 1.26813                      | 1 |
| SharpSat   | HiddenTautologyElimination                | 0.0014236           | 0.00207615        | 0.00349975       | 1.24593                      | 1 |
| SharpSat   | HyperBinaryResolution                     | 0.00137711          | 0.00216317        | 0.00354028       | 1.23167                      | 1 |
| SharpSat   | EquivalentLiteralElimination              | 0.00167346          | 0.00197601        | 0.00364947       | 1.19481                      | 1 |
| SharpSat   | BinaryResolution                          | 0.00135112          | 0.00236773        | 0.00371885       | 1.17252                      | 1 |
| SharpSat   | NoPreprocessor                            | 0.00216937          | 0.00219107        | 0.00436044       | 1                            | 1 |
| DSharp     | NoPreprocessor                            | 0.0011797           | 0.00331235        | 0.00449204       | 1                            | 1 |
| DSharp     | UnitPropagation                           | 0.0015347           | 0.00326991        | 0.00480461       | 0.934944                     | 1 |
| DSharp     | SharpSatPreprocessor                      | 0.00161314          | 0.00330472        | 0.00491786       | 0.913414                     | 1 |
| DSharp     | EquivalentLiteralElimination              | 0.00166154          | 0.00336099        | 0.00502253       | 0.89438                      | 1 |
| DSharp     | HiddenTautologyElimination                | 0.00158167          | 0.00344729        | 0.00502896       | 0.893235                     | 1 |
| DSharp     | Subsumption                               | 0.00161457          | 0.00348735        | 0.00510192       | 0.880462                     | 1 |
| DSharp     | HyperBinaryResolution                     | 0.0016191           | 0.00348926        | 0.00510836       | 0.879352                     | 1 |
| DSharp     | Probing                                   | 0.00154543          | 0.00379539        | 0.00534081       | 0.841079                     | 1 |
| DSharp     | BinaryResolution                          | 0.00172949          | 0.00391936        | 0.00564885       | 0.795214                     | 1 |
| Ganak      | NoPreprocessor                            | 0.00420475          | 0.00200343        | 0.00620818       | 1                            | 1 |
| D4         | NoPreprocessor                            | 0.00135994          | 0.0050993         | 0.00645924       | 1                            | 1 |
| D4         | Subsumption                               | 0.0019269           | 0.00490189        | 0.00682878       | 0.945884                     | 1 |
| D4         | UnitPropagation                           | 0.00176263          | 0.00508571        | 0.00684834       | 0.943183                     | 1 |
| D4         | BinaryResolution                          | 0.00184703          | 0.00505686        | 0.00690389       | 0.935594                     | 1 |
| D4         | EquivalentLiteralElimination              | 0.00186682          | 0.00508428        | 0.00695109       | 0.92924                      | 1 |
| D4         | SharpSatPreprocessor                      | 0.00190496          | 0.00511742        | 0.00702238       | 0.919807                     | 1 |
| D4         | HiddenTautologyElimination                | 0.00221753          | 0.00521922        | 0.00743675       | 0.868556                     | 1 |
| D4         | HyperBinaryResolution                     | 0.00213218          | 0.00531244        | 0.00744462       | 0.867638                     | 1 |
| D4         | Probing                                   | 0.00198221          | 0.00570512        | 0.00768733       | 0.840244                     | 1 |
| BddMiniSat | EquivalentLiteralElimination              | 0.00200176          | 0.0204277         | 0.0224295        | 3.20768                      | 1 |
| CountAntom | BinaryResolution                          | 0.00138855          | 0.0559335         | 0.057322         | 1.00806                      | 1 |
| CountAntom | HiddenTautologyElimination                | 0.00159478          | 0.0558348         | 0.0574296        | 1.00617                      | 1 |
| CountAntom | EquivalentLiteralElimination              | 0.00166535          | 0.0560009         | 0.0576663        | 1.00204                      | 1 |
| CountAntom | UnitPropagation                           | 0.00134254          | 0.0563865         | 0.057729         | 1.00095                      | 1 |
| CountAntom | Subsumption                               | 0.00152397          | 0.056215          | 0.057739         | 1.00078                      | 1 |
| CountAntom | NoPreprocessor                            | 0.00100183          | 0.0567822         | 0.0577841        | 1                            | 1 |
| CountAntom | Probing                                   | 0.00159311          | 0.056406          | 0.0579991        | 0.996292                     | 1 |
| CountAntom | SharpSatPreprocessor                      | 0.00163674          | 0.0576336         | 0.0592704        | 0.974923                     | 1 |
| BddMiniSat | HiddenTautologyElimination                | 0.00210071          | 0.0574172         | 0.0595179        | 1.20882                      | 1 |
| CountAntom | HyperBinaryResolution                     | 0.00398207          | 0.0630298         | 0.0670118        | 0.862297                     | 1 |
| BddMiniSat | SharpSatPreprocessor                      | 0.00170732          | 0.0661881         | 0.0678954        | 1.05967                      | 1 |
| BddMiniSat | UnitPropagation                           | 0.00171089          | 0.0674126         | 0.0691235        | 1.04084                      | 1 |
| BddMiniSat | Subsumption                               | 0.00212455          | 0.0670786         | 0.0692031        | 1.03964                      | 1 |
| BddMiniSat | BinaryResolution                          | 0.00170445          | 0.0678906         | 0.0695951        | 1.03379                      | 1 |
| BddMiniSat | HyperBinaryResolution                     | 0.00178552          | 0.0689485         | 0.070734         | 1.01714                      | 1 |
| BddMiniSat | NoPreprocessor                            | 0.00409508          | 0.0678515         | 0.0719466        | 1                            | 1 |
| BddMiniSat | Probing                                   | 0.00202894          | 0.0704665         | 0.0724955        | 0.992429                     | 1 |

For this problem no preprocessing offers a performance improvement.

## financial_services

Running all registered solvers with all registered preprocessors on all files in the financial_services directory using a timeout of 30s leads to the following results table:

| Solver     | Preprocessor                 | Avg. preprocessor time   | Avg. solver time     | Avg. total time      | Avg. speedup         | Percentage finished |
| ---------- | ---------------------------- | ------------------------ | -------------------- | -------------------- | ------------------   | --------------------- |
| SharpSat   | NoPreprocessor               | 0.001453399658203125     | 0.03670525550842285  | 0.03815865516662598  | 1.0                                    | 1 |
| SharpSat   | EquivalentLiteralElimination | 0.010097742080688477     | 0.0303652286529541   | 0.04046297073364258  | 0.9430512509280319                     | 1 |
| SharpSat   | BinaryResolution             | 0.00862574577331543      | 0.033850908279418945 | 0.042476654052734375 | 0.8983441850022452                     | 1 |
| SharpSat   | UnitPropagation              | 0.008490800857543945     | 0.034151554107666016 | 0.04264235496520996  | 0.8948533728439239                     | 1 |
| SharpSat   | Probing                      | 0.00842142105102539      | 0.03433084487915039  | 0.04275226593017578  | 0.8925528117959357                     | 1 |
| Ganak      | BinaryResolution             | 0.008567333221435547     | 0.0349423885345459   | 0.043509721755981445 | 1.0317765612927619                     | 1 |
| Ganak      | UnitPropagation              | 0.00862741470336914      | 0.03493165969848633  | 0.04355907440185547  | 1.030607553366174                      | 1 |
| Ganak      | HyperBinaryResolution        | 0.010509967803955078     | 0.033455848693847656 | 0.043965816497802734 | 1.0210730670368644                     | 1 |
| Ganak      | Probing                      | 0.008392810821533203     | 0.0357668399810791   | 0.044159650802612305 | 1.0165911704522754                     | 1 |
| Ganak      | NoPreprocessor               | 0.00882101058959961      | 0.0360713005065918   | 0.044892311096191406 | 1.0                                    | 1 |
| Ganak      | Subsumption                  | 0.010593891143798828     | 0.03500795364379883  | 0.045601844787597656 | 0.984440680092854                      | 1 |
| Ganak      | EquivalentLiteralElimination | 0.011517763137817383     | 0.034127235412597656 | 0.04564499855041504  | 0.9835099687122941                     | 1 |
| SharpSat   | Subsumption                  | 0.010399580001831055     | 0.03540444374084473  | 0.04580402374267578  | 0.8330852193466447                     | 1 |
| Ganak      | HiddenTautologyElimination   | 0.010396957397460938     | 0.036821603775024414 | 0.04721856117248535  | 0.9507344142106247                     | 1 |
| SharpSat   | HyperBinaryResolution        | 0.009373903274536133     | 0.038460731506347656 | 0.04783463478088379  | 0.7977202155178859                     | 1 |
| SharpSat   | HiddenTautologyElimination   | 0.011445283889770508     | 0.03816962242126465  | 0.049614906311035156 | 0.7690965881787603                     | 1 |
| SharpSat   | SharpSatPreprocessor         | 0.019812822341918945     | 0.03534507751464844  | 0.05515789985656738  | 0.6918076153344082                     | 1 |
| Ganak      | SharpSatPreprocessor         | 0.019446134567260742     | 0.0365443229675293   | 0.05599045753479004  | 0.801785037536035                      | 1 |
| D4         | HiddenTautologyElimination   | 0.04405093193054199      | 0.10706281661987305  | 0.15111374855041504  | 1.1315537450084172                     | 1 |
| D4         | BinaryResolution             | 0.04952812194824219      | 0.10889148712158203  | 0.15841960906982422  | 1.0793697137525209                     | 1 |
| D4         | Probing                      | 0.054320335388183594     | 0.10662341117858887  | 0.16094374656677246  | 1.0624415781419665                     | 1 |
| D4         | UnitPropagation              | 0.048589229583740234     | 0.11461257934570312  | 0.16320180892944336  | 1.0477416225723795                     | 1 |
| D4         | NoPreprocessor               | 0.06178712844848633      | 0.1092061996459961   | 0.17099332809448242  | 1.0                                    | 1 |
| D4         | EquivalentLiteralElimination | 0.0632028579711914       | 0.10837435722351074  | 0.17157721519470215  | 0.9965969426677246                     | 1 |
| D4         | HyperBinaryResolution        | 0.05169534683227539      | 0.12679457664489746  | 0.17848992347717285  | 0.9579998958112099                     | 1 |
| D4         | SharpSatPreprocessor         | 0.06727242469787598      | 0.11166024208068848  | 0.17893266677856445  | 0.9556294620372073                     | 1 |
| D4         | Subsumption                  | 0.04822945594787598      | 0.15009498596191406  | 0.19832444190979004  | 0.8621898866719642                     | 1 |
| DSharp     | HyperBinaryResolution        | 0.010323524475097656     | 0.2677500247955322   | 0.2780735492706299   | 1.4553190577240478                     | 1 |
| RelSat     | NoPreprocessor               | 0.0015590190887451172    | 0.28327393531799316  | 0.2848329544067383   | 1.0                                    | 1 |
| RelSat     | BinaryResolution             | 0.008370637893676758     | 0.2847163677215576   | 0.2930870056152344   | 0.9718375395348232                     | 1 |
| RelSat     | Subsumption                  | 0.011641263961791992     | 0.28233790397644043  | 0.2939791679382324   | 0.968888225667011                      | 1 |
| RelSat     | UnitPropagation              | 0.008223772048950195     | 0.2861452102661133   | 0.2943689823150635   | 0.9676051877703651                     | 1 |
| RelSat     | Probing                      | 0.008456230163574219     | 0.28595542907714844  | 0.29441165924072266  | 0.9674649269710054                     | 1 |
| RelSat     | EquivalentLiteralElimination | 0.01038360595703125      | 0.2859532833099365   | 0.2963368892669678   | 0.961179538299514                      | 1 |
| RelSat     | HyperBinaryResolution        | 0.00985860824584961      | 0.2876279354095459   | 0.2974865436553955   | 0.9574650029773616                     | 1 |
| RelSat     | SharpSatPreprocessor         | 0.019819021224975586     | 0.2809011936187744   | 0.30072021484375     | 0.9471692967322914                     | 1 |
| RelSat     | HiddenTautologyElimination   | 0.010166406631469727     | 0.2961156368255615   | 0.30628204345703125  | 0.9299694856146469                     | 1 |
| DSharp     | Probing                      | 0.009990215301513672     | 0.32927465438842773  | 0.3392648696899414   | 1.1928312414791493                     | 1 |
| DSharp     | Subsumption                  | 0.010635852813720703     | 0.3380146026611328   | 0.3486504554748535   | 1.1607205134762908                     | 1 |
| DSharp     | HiddenTautologyElimination   | 0.010329246520996094     | 0.35804033279418945  | 0.36836957931518555  | 1.0985861982817429                     | 1 |
| DSharp     | SharpSatPreprocessor         | 0.01934981346130371      | 0.3506746292114258   | 0.3700244426727295   | 1.093672982193886                      | 1 |
| DSharp     | BinaryResolution             | 0.008996963500976562     | 0.38161611557006836  | 0.3906130790710449   | 1.0360271004364148                     | 1 |
| DSharp     | UnitPropagation              | 0.008790254592895508     | 0.3851144313812256   | 0.3939046859741211   | 1.0273696914819181                     | 1 |
| DSharp     | NoPreprocessor               | 0.002596139907836914     | 0.40208959579467773  | 0.40468573570251465  | 1.0                                    | 1 |
| DSharp     | EquivalentLiteralElimination | 0.010515213012695312     | 0.45986318588256836  | 0.47037839889526367  | 0.8603408163575632                     | 1 |
| CountAntom | EquivalentLiteralElimination | 0.021288156509399414     | 1.2726249694824219   | 1.2939131259918213   | 1.221418022448598                      | 1 |
| CountAntom | HyperBinaryResolution        | 0.010887861251831055     | 1.3524808883666992   | 1.3633687496185303   | 1.1591939539551652                     | 1 |
| CountAntom | HiddenTautologyElimination   | 0.010915040969848633     | 1.526231050491333    | 1.5371460914611816   | 1.0281448330437528                     | 1 |
| CountAntom | Probing                      | 0.008284568786621094     | 1.5494515895843506   | 1.5577361583709717   | 1.0145548737996506                     | 1 |
| CountAntom | Subsumption                  | 0.011606454849243164     | 1.551887035369873    | 1.5634934902191162   | 1.010818926625481                      | 1 |
| CountAntom | SharpSatPreprocessor         | 0.01945042610168457      | 1.5506103038787842   | 1.5700607299804688   | 1.0065908798246765                     | 1 |
| CountAntom | UnitPropagation              | 0.00859212875366211      | 1.561903715133667    | 1.570495843887329    | 1.0063119986725644                     | 1 |
| CountAntom | BinaryResolution             | 0.009241819381713867     | 1.5652284622192383   | 1.5744702816009521   | 1.0037717637720183                     | 1 |
| CountAntom | NoPreprocessor               | 0.01985931396484375      | 1.5605494976043701   | 1.5804088115692139   | 1.0                                    | 1 |
| BddMiniSat | BinaryResolution             | No run finished          | No run finished      | No run finished      | No data                                | 0 |
| BddMiniSat | EquivalentLiteralElimination | No run finished          | No run finished      | No run finished      | No data                                | 0 |
| BddMiniSat | HiddenTautologyElimination   | No run finished          | No run finished      | No run finished      | No data                                | 0 |
| BddMiniSat | HyperBinaryResolution        | No run finished          | No run finished      | No run finished      | No data                                | 0 |
| BddMiniSat | NoPreprocessor               | No run finished          | No run finished      | No run finished      | No data                                | 0 |
| BddMiniSat | Probing                      | No run finished          | No run finished      | No run finished      | No data                                | 0 |
| BddMiniSat | SharpSatPreprocessor         | No run finished          | No run finished      | No run finished      | No data                                | 0 |
| BddMiniSat | Subsumption                  | No run finished          | No run finished      | No run finished      | No data                                | 0 |
| BddMiniSat | UnitPropagation              | No run finished          | No run finished      | No run finished      | No data                                | 0 |

Hidden Tautology Elimination leads to a small performance improvement for d4, several preprocessings including Hyper Binary Resolution, Probing, Subsumption, Hidden Tautology Elimination and the SharpSAT preprocessor lead to small performance improvements for dsharp and Equivalent Literal Elimination and Hyper Binary Resolution lead to small performance improvements for countAntom. For all other solvers, preprocessings lead to performance deterioration.

## KConfig

Running all registered solvers with all registered preprocessors on all files in the KConfig directory using a timeout of 60s leads to the following results table:

| Solver     | Preprocessor                   | Avg. preprocessor time   | Avg. solver time   | Avg. total time   | Avg. speedup   | Percentage finished |
| ---------- | ----------------------------   | ------------------------ | ------------------ | ----------------- | -------------- | --------------------- |
| BddMiniSat | EquivalentLiteralElimination               | 0.00193357         | 0.00435877        | 0.00629234       | 6.92983               | 0.166667 |
| SharpSat   | NoPreprocessor                             | 0.00178146         | 0.00729918        | 0.00908065       | 1                     | 0.833333 |
| SharpSat   | EquivalentLiteralElimination               | 0.00482578         | 0.00441403        | 0.00923982       | 0.982774              | 0.833333 |
| SharpSat   | Subsumption                                | 0.00434909         | 0.00557766        | 0.00992675       | 0.914766              | 0.833333 |
| SharpSat   | HiddenTautologyElimination                 | 0.00461535         | 0.00541372        | 0.0100291        | 0.905432              | 0.833333 |
| Ganak      | EquivalentLiteralElimination               | 0.00499783         | 0.00505996        | 0.0100578        | 2.98458               | 0.833333 |
| SharpSat   | BinaryResolution                           | 0.004285           | 0.00635648        | 0.0106415        | 0.853326              | 0.833333 |
| Ganak      | HiddenTautologyElimination                 | 0.00474153         | 0.00596824        | 0.0107098        | 2.80289               | 0.833333 |
| SharpSat   | UnitPropagation                            | 0.00408835         | 0.00664339        | 0.0107317        | 0.846148              | 0.833333 |
| Ganak      | BinaryResolution                           | 0.00425053         | 0.0069726         | 0.0112231        | 2.67468               | 0.833333 |
| SharpSat   | Probing                                    | 0.00433087         | 0.00691648        | 0.0112473        | 0.807359              | 0.833333 |
| SharpSat   | HyperBinaryResolution                      | 0.00440984         | 0.00716844        | 0.0115783        | 0.784283              | 0.833333 |
| Ganak      | HyperBinaryResolution                      | 0.00452852         | 0.00761361        | 0.0121421        | 2.47224               | 0.833333 |
| Ganak      | Subsumption                                | 0.00474987         | 0.00759611        | 0.012346         | 2.43142               | 0.833333 |
| Ganak      | UnitPropagation                            | 0.00447826         | 0.00803599        | 0.0125143        | 2.39872               | 0.833333 |
| SharpSat   | SharpSatPreprocessor                       | 0.00731673         | 0.00555248        | 0.0128692        | 0.70561               | 0.833333 |
| Ganak      | Probing                                    | 0.00443821         | 0.00870996        | 0.0131482        | 2.28307               | 0.833333 |
| Ganak      | SharpSatPreprocessor                       | 0.00813684         | 0.00650907        | 0.0146459        | 2.0496                | 0.833333 |
| RelSat     | SharpSatPreprocessor                       | 0.00437355         | 0.0106908         | 0.0150643        | 1.12406               | 0.5      |
| RelSat     | EquivalentLiteralElimination               | 0.00485706         | 0.0113905         | 0.0162476        | 1.0422                | 0.833333 |
| RelSat     | HiddenTautologyElimination                 | 0.00497079         | 0.0118558         | 0.0168266        | 1.00633               | 0.666667 |
| RelSat     | NoPreprocessor                             | 0.00194287         | 0.0149903         | 0.0169331        | 1                     | 0.666667 |
| RelSat     | UnitPropagation                            | 0.00448817         | 0.0125608         | 0.017049         | 0.993207              | 0.666667 |
| RelSat     | BinaryResolution                           | 0.00451392         | 0.0126241         | 0.0171381        | 0.988043              | 0.666667 |
| RelSat     | Subsumption                                | 0.00498843         | 0.0124624         | 0.0174508        | 0.970336              | 0.666667 |
| RelSat     | HyperBinaryResolution                      | 0.00500166         | 0.0130879         | 0.0180895        | 0.936074              | 0.666667 |
| DSharp     | SharpSatPreprocessor                       | 0.00742588         | 0.011088          | 0.0185139        | 1.19338               | 0.833333 |
| BddMiniSat | SharpSatPreprocessor                       | 0.00179768         | 0.0167968         | 0.0185945        | 2.34504               | 0.166667 |
| RelSat     | Probing                                    | 0.0049504          | 0.0138527         | 0.0188031        | 0.90055               | 0.666667 |
| DSharp     | HiddenTautologyElimination                 | 0.0046699          | 0.0141339         | 0.0188038        | 1.17498               | 0.833333 |
| DSharp     | EquivalentLiteralElimination               | 0.00542159         | 0.013458          | 0.0188796        | 1.17026               | 0.833333 |
| DSharp     | BinaryResolution                           | 0.00482326         | 0.0155452         | 0.0203685        | 1.08472               | 0.833333 |
| DSharp     | NoPreprocessor                             | 0.00275378         | 0.0193403         | 0.0220941        | 1                     | 0.833333 |
| DSharp     | HyperBinaryResolution                      | 0.00456362         | 0.0175615         | 0.0221251        | 0.998595              | 0.833333 |
| DSharp     | Subsumption                                | 0.00503693         | 0.0178505         | 0.0228875        | 0.965334              | 0.833333 |
| DSharp     | Probing                                    | 0.00470042         | 0.0199259         | 0.0246264        | 0.897171              | 0.833333 |
| DSharp     | UnitPropagation                            | 0.00445962         | 0.0202981         | 0.0247577        | 0.892411              | 0.833333 |
| D4         | SharpSatPreprocessor                       | 0.0122576          | 0.0168779         | 0.0291355        | 1.57291               | 0.833333 |
| D4         | BinaryResolution                           | 0.0103321          | 0.0188328         | 0.0291649        | 1.57133               | 0.833333 |
| D4         | HiddenTautologyElimination                 | 0.0113268          | 0.0181447         | 0.0294715        | 1.55498               | 0.833333 |
| Ganak      | NoPreprocessor                             | 0.0208673          | 0.00915089        | 0.0300182        | 1                     | 0.833333 |
| D4         | EquivalentLiteralElimination               | 0.0131453          | 0.0186251         | 0.0317704        | 1.44246               | 0.833333 |
| D4         | HyperBinaryResolution                      | 0.0146301          | 0.0193442         | 0.0339743        | 1.34889               | 0.833333 |
| D4         | UnitPropagation                            | 0.014511           | 0.0205466         | 0.0350576        | 1.30721               | 0.833333 |
| BddMiniSat | Subsumption                                | 0.00174332         | 0.0349524         | 0.0366957        | 1.18828               | 0.166667 |
| BddMiniSat | HiddenTautologyElimination                 | 0.0016861          | 0.0357866         | 0.0374727        | 1.16364               | 0.166667 |
| D4         | Probing                                    | 0.0161394          | 0.0221166         | 0.038256         | 1.19792               | 0.833333 |
| BddMiniSat | UnitPropagation                            | 0.00176644         | 0.0372987         | 0.0390651        | 1.11621               | 0.166667 |
| BddMiniSat | BinaryResolution                           | 0.00166368         | 0.0374362         | 0.0390999        | 1.11522               | 0.166667 |
| BddMiniSat | Probing                                    | 0.00169706         | 0.0386412         | 0.0403383        | 1.08098               | 0.166667 |
| D4         | Subsumption                                | 0.0192191          | 0.0221129         | 0.041332         | 1.10877               | 0.833333 |
| BddMiniSat | HyperBinaryResolution                      | 0.001755           | 0.0411637         | 0.0429187        | 1.01599               | 0.166667 |
| BddMiniSat | NoPreprocessor                             | 0.00318718         | 0.0404177         | 0.0436049        | 1                     | 0.166667 |
| D4         | NoPreprocessor                             | 0.0240132          | 0.0218144         | 0.0458276        | 1                     | 0.833333 |
| CountAntom | Subsumption                                | 0.00475454         | 0.0758615         | 0.0806161        | 1.68098               | 0.833333 |
| CountAntom | HiddenTautologyElimination                 | 0.00439095         | 0.0892434         | 0.0936344        | 1.44727               | 0.833333 |
| CountAntom | UnitPropagation                            | 0.00435209         | 0.128164          | 0.132516         | 1.02262               | 0.833333 |
| CountAntom | Probing                                    | 0.00437346         | 0.128399          | 0.132772         | 1.02065               | 0.833333 |
| CountAntom | EquivalentLiteralElimination               | 0.0079289          | 0.124991          | 0.13292          | 1.01952               | 0.833333 |
| CountAntom | BinaryResolution                           | 0.00432439         | 0.130032          | 0.134357         | 1.00861               | 0.833333 |
| CountAntom | NoPreprocessor                             | 0.00920081         | 0.126313          | 0.135514         | 1                     | 0.833333 |
| CountAntom | SharpSatPreprocessor                       | 0.00847707         | 0.129339          | 0.137816         | 0.9833                | 0.833333 |
| CountAntom | HyperBinaryResolution                      | 0.0104416          | 0.131625          | 0.142066         | 0.953881              | 0.833333 |

This problem set included `linux-2.6.33.3.dimacs` which not a single solver was able to solve. Note that while bddminisat with the Equivalent Literal Elimination resulted in the shortest average time it was only able to solve the easiest 16% of the problems and should therefore be interpreted as an outlier.

For sharpsat no preprocessing lead to a performance improvement. For ganak all preprocessings lead to >2x performance improvements. For relsat only the SharpSAT preprocessor lead to a notable improvement. For dsharp and d4 some preprocessings lead to a performance improvements for example Hidden Tautology Elimination, while other preprocessings lead to performance deterioration. bddminisat's performance is improved by all preprocessings, the improvements using Equivalent Literal Elimination and the SharpSAT preprocessor are especially notable.
