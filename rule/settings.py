post_surgery_total_stage_rule = [
    {
        "A=yp": [
            {
                "C=T4b | D=N3": [
                    "IVA"
                ]
            },
            {
                "C=T4a & D!=N0": [
                    "IVA"
                ]
            },
            {
                "C=T4a & D=N0": [
                    "IIIB"
                ]
            },
            {
                "D=N2": [
                    "IIIB"
                ]
            },
            {
                "C=T3 & D=N1": [
                    "IIIB"
                ]
            },
            {
                "D=N1": [
                    "IIIA"
                ]
            },
            {
                "C=T3 & D=N0": [
                    "II"
                ]
            },
            {
                "D=N0": [
                    "I"
                ]
            }
        ]
    },
    {
        "A=p & B!=[腺癌]": [
            {
                "C=T4b | D=N3": [
                    "IVA"
                ]
            },
            {
                "C=T4a & D=N2": [
                    "IVA"
                ]
            },
            {
                "C=T4a & (D=N0 | D=N1)": [
                    "IIIB"
                ]
            },
            {
                "C=T3 & (D=N1 | D=N2)": [
                    "IIIB"
                ]
            },
            {
                "C=T2 & D=N2": [
                    "IIIB"
                ]
            },
            {
                "C=T2 & D=N1": [
                    "IIIA"
                ]
            },
            {
                "C=T1 & D=N2": [
                    "IIIA"
                ]
            },
            {
                "C=T1 & D=N1": [
                    "IIB"
                ]
            },
            {
                "C=T3 & D=N0": [
                    {
                        "F=食管胸下段 & E!=分化不能评估（Gx）": [
                            "IIA"
                        ]
                    },
                    {
                        "F in [颈段,食管胸上段,食管胸中段] & E=高分化（G1）": [
                            "IIA"
                        ]
                    },
                    "IIB"
                ]
            },
            {
                "C=T2 & D=N0": [
                    {
                        "E=高分化（G1）": [
                            "IB"
                        ]
                    },
                    "IIA"
                ]
            },
            {
                "C=T1b & D=N0": [
                    "IB"
                ]
            },
            {
                "C=T1a & D=N0": [
                    {
                        "E in [高-中分化（G1-G2）,中分化（G2）,中-低分化（G2-G3）,低分化或未分化（G3）]": [
                            "IB"
                        ]
                    },
                    "IA"
                ]
            },
            {
                "C=Tis & D=N0": [
                    "0"
                ]
            }
        ]
    },
    {
        "A=p & (B=[腺癌] | F=胃食管交界)": [
            {
                "C=T4b | D=N3": [
                    "IVA"
                ]
            },
            {
                "C=T4a & D=N2": [
                    "IVA"
                ]
            },
            {
                "C=T4a & (D=N0 | D=N1)": [
                    "IIIB"
                ]
            },
            {
                "C=T3 & (D=N1 | D=N2)": [
                    "IIIB"
                ]
            },
            {
                "C=T2 & D=N2": [
                    "IIIB"
                ]
            },
            {
                "C=T2 & D=N1": [
                    "IIIA"
                ]
            },
            {
                "C=T1 & D=N2": [
                    "IIIA"
                ]
            },
            {
                "C=T1 & D=N1": [
                    "IIB"
                ]
            },
            {
                "C=T3 & D=N0": [
                    "IIB"
                ]
            },
            {
                "C=T2 & D=N0": [
                    {
                        "E in [高分化（G1）,高-中分化（G1-G2）,中分化（G2）]": [
                            "IC"
                        ]
                    },
                    "IIA"
                ]
            },
            {
                "(C=T1a | C=T1b) & D=N0": [
                    {
                        "E in [中-低分化（G2-G3）,低分化或未分化（G3）]": [
                            "IC"
                        ]
                    }
                ]
            },
            {
                "C=T1b": [
                    "IB"
                ]
            },
            {
                "C=T1a & E in [高-中分化（G1-G2）,中分化（G2）]": [
                    "IB"
                ]
            },
            {
                "C=T1a": [
                    "IA"
                ]
            },
            {
                "C=Tis & D=N0": [
                    "0"
                ]
            }
        ]
    }
]

after_neoadjuvant_total_stage_rule = [
    {
        "A!=[腺癌] & A!=[]": [
            {
                "D=M1": [
                    "IVB"
                ]
            },
            {
                "D=M0": [
                    {
                        "B in [T4a,T4b]": [
                            "IVA"
                        ]
                    }
                ]
            },
            {
                "B=T3 & C=N1": [
                    "III"
                ]
            },
            {
                "B=T3 & C=N0": [
                    "II"
                ]
            },
            {
                "B=T2": [
                    "II"
                ]
            },
            {
                "B=T1": [
                    "I"
                ]
            }
        ]
    },
    {
        "A=[腺癌] | E=[胃食管交界]": [
            {
                "D=M1": [
                    "IVB"
                ]
            },
            {
                "D=M0": [
                    {
                        "B=T4b": [
                            "IVA"
                        ]
                    },
                    {
                        "B in [T4a,T3]": [
                            "III"
                        ]
                    },
                    {
                        "B=T2 & C=N1": [
                            "III"
                        ]
                    },
                    {
                        "B=T2 & C=N0": [
                            "IIB"
                        ]
                    },
                    {
                        "B=T1 & C=N1": [
                            "IIA"
                        ]
                    },
                    {
                        "B=T1 & C=N0": [
                            "I"
                        ]
                    }
                ]
            }
        ]
    }
]

t_stage_rule = [
    {
        "B contains [主动脉,椎体,气管,隆凸,左主支气管,右主支气管,下肺静脉,肺组织,腹腔动脉干,下腔静脉,乳糜池]": [
            "T4b"
        ]
    },
    {
        "B contains [胸膜,心包,膈肌,腹膜,胸导管,迷走神经,左侧喉返神经,右侧喉返神经,奇静脉,胃体,胃小弯,胃大弯,胃底]": [
            "T4a"
        ]
    },
    {
        "C contains [外膜层,全层,周围组织]": [
            "T3"
        ]
    },
    {
        "C contains [肌层,固有肌层,浅肌层,深肌层]": [
            "T2"
        ]
    },
    {
        "C contains [粘膜下层]": [
            "T1b"
        ]
    },
    {
        "C contains [粘膜固有层,粘膜肌层]": [
            "T1a"
        ]
    },
    {
        "E not contains [MR] & D contains [胃镜] & D not contains [超声胃镜]": [
            "T3"
        ]
    }
]