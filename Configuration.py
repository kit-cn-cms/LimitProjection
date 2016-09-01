#set up everything here

doParallel = True

doProjection = False
doCombineDataCards = True
doScaleToProjection = True
doCalulation = True
doOutputParsing = True
doPlotLimits = True

projectionName              = [ 'nominal', 'lumi5', 'lumi10', 'lumi20', 'lumi30', 'lumi40', 'lumi50', 'lumi60', 'lumi70', 'lumi80', 'lumi90', 'lumi100' ]
projectionLuminosity        = [ 2.7, 5.0, 10.0, 20.0, 30.0 ,40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0 ]
projectionFactorTheorySyst  = [ 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 ]

scaleStatSyst = False

inputDir='/nfs/dust/cms/user/shwillia/Moriond/LimitProjection/datacards/'

outputDir='/nfs/dust/cms/user/shwillia/Moriond/LimitProjection/output/'

dataCards = [ 'ttH_hbb_13TeV_sl_j4_t3.txt',
              'ttH_hbb_13TeV_sl_j4_t4_high.txt',
              'ttH_hbb_13TeV_sl_j4_t4_low.txt',
              'ttH_hbb_13TeV_sl_j5_t3.txt',
              'ttH_hbb_13TeV_sl_j5_tge4_high.txt',
              'ttH_hbb_13TeV_sl_j5_tge4_low.txt',
              'ttH_hbb_13TeV_sl_jge6_t2.txt',
              'ttH_hbb_13TeV_sl_jge6_t3.txt',
              'ttH_hbb_13TeV_sl_jge6_tge4_high.txt',
              'ttH_hbb_13TeV_sl_jge6_tge4_low.txt',
              'ttH_hbb_13TeV_sl_boosted.txt'
            ]
            
dataCardNames = [ 'ttH_hbb_13TeV_sl_4j3t',
                  'ttH_hbb_13TeV_sl_4j4t_high',
                  'ttH_hbb_13TeV_sl_4j4t_low',
                  'ttH_hbb_13TeV_sl_5j3t',
                  'ttH_hbb_13TeV_sl_5jge4t_high',
                  'ttH_hbb_13TeV_sl_5jge4t_low',
                  'ttH_hbb_13TeV_sl_ge6j2t',
                  'ttH_hbb_13TeV_sl_ge6j3t',
                  'ttH_hbb_13TeV_sl_ge6jge4t_high',
                  'ttH_hbb_13TeV_sl_ge6jge4t_low',
                  'ttH_hbb_13TeV_sl_boosted'
                ]
                
omittedSysts = []

histograms = 'common/ttH_hbb_13TeV_sl.root'

allSysts  = [ "lumi_13TeV",
              "QCDscale_ttH",
              "QCDscale_ttbar",
              "QCDscale_singlet",
              "QCDscale_V",
              "QCDscale_VV",
              "pdf_gg_ttH",
              "pdf_gg",
              "pdf_qqbar",
              "pdf_qg",
              "CMS_ttH_Q2scale_ttbarOther",
              "CMS_ttH_Q2scale_ttbarPlusB",
              "CMS_ttH_Q2scale_ttbarPlus2B",
              "CMS_ttH_Q2scale_ttbarPlusBBbar",
              "CMS_ttH_Q2scale_ttbarPlusCCbar",
              "CMS_ttH_CSVLF",
              "CMS_ttH_CSVHF",
              "CMS_ttH_CSVHFStats1",
              "CMS_ttH_CSVLFStats1",
              "CMS_ttH_CSVHFStats2",
              "CMS_ttH_CSVLFStats2",
              "CMS_ttH_CSVCErr1",
              "CMS_ttH_CSVCErr2",
              "CMS_scale_j",
              "CMS_ttH_QCDscale_ttbarPlusB",
              "CMS_ttH_QCDscale_ttbarPlus2B",
              "CMS_ttH_QCDscale_ttbarPlusBBbar",
              "CMS_ttH_QCDscale_ttbarPlusCCbar",
              "CMS_ttH_PU",
              "CMS_res_j",
              "CMS_ttH_eff_leptonLJ",
              "CMS_ttH_ljets_Trig",
              "CMS_ttH_PSscale_ttbarOther",
              "CMS_ttH_PSscale_ttbarPlusB",
              "CMS_ttH_PSscale_ttbarPlus2B",
              "CMS_ttH_PSscale_ttbarPlusBBbar",
              "CMS_ttH_PSscale_ttbarPlusCCbar",
              "CMS_ttH_dl_Trig",
              "CMS_ttH_eff_lepton"
            ]

statSysts = [ "CMS_ttH_CSVHFStats1",
              "CMS_ttH_CSVLFStats1",
              "CMS_ttH_CSVHFStats2",
              "CMS_ttH_CSVLFStats2"
            ]

theoSysts = [ "QCDscale_ttH",
              "QCDscale_ttbar",
              "QCDscale_singlet",
              "QCDscale_V",
              "QCDscale_VV",
              "pdf_gg_ttH",
              "pdf_gg",
              "pdf_qqbar",
              "pdf_qg",
              "CMS_ttH_QCDscale_ttbarPlusB",
              "CMS_ttH_QCDscale_ttbarPlus2B",
              "CMS_ttH_QCDscale_ttbarPlusBBbar",
              "CMS_ttH_QCDscale_ttbarPlusCCbar"
            ]
