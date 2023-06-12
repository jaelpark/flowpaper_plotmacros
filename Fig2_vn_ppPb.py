
import numpy as np
import ROOT

import scipy
from scipy import interpolate

import sys
sys.path.append("JPyPlotRatio");
#https://github.com/jaelpark/JPyPlotRatio


import JPyPlotRatio


f = ROOT.TFile("data/Final_Items.root","read");
fpPb = ROOT.TFile("data/fout_v2_pPb_v2.root","read");
dataTypePlotParams = [
	{'plotType':'data','color':'r','fmt':'o','markersize':5.0},
	{'plotType':'data','color':'g','fmt':'d','fillstyle':'none','markersize':5.0},
	{'plotType':'data','color':'b','fmt':'D','fillstyle':'none','markersize':5.0},
	{'plotType':'theory','facecolor':'C0','edgecolor':'C0','alpha':0.5,'linestyle':'solid','linecolor':'C0'},
	{'plotType':'theory','facecolor':'C1','edgecolor':'C1','alpha':0.5,'linestyle':'dotted','linecolor':'C1'},
	{'plotType':'theory','facecolor':'C2','edgecolor':'C2','alpha':0.5,'linestyle':'dashed','linecolor':'C2'},
	{'plotType':'theory','facecolor':'C3','edgecolor':'C3','alpha':0.5,'linestyle':'dashdot','linecolor':'C3'},
];

#adding pPb?
addpPb = True;
# define panel/xaxis limits/titles
nrow = 1;
ncol = 2;
xlimits = [(0.8,3.8),(0.8,3.8)];
ylimits = [(0.005,0.175)];
rlimits = [(0.3,1.9),(0.,4.5)];


# add here the histogram names for each pad
histnames =      ["v2_pt_stat","v3_pt_stat"]; #LP,jet  # check it with ROOT file Title
histnamesSyst =  ["v2_pt_syst","v3_pt_syst"]; #LP,jet  # check it with ROOT file Title	
histnamesModels = [ "v2_EPOS","v3_EPOS" ];	

histatlas_stat = ["v2_atlas_stat","v3_atlas_stat"];
histatlas_syst = ["v2_atlas_syst","v3_atlas_syst"];

histpPb_stat = ["v2_v0a_stat_pt","v3_v0a_stat_pt"];
histpPb_syst = ["v2_v0a_syst_pt_sm","v3_v0a_syst_pt"];
# add labels for each pad
#plables = [ "Leading Particle $|\\eta|<0.9$","Jet, anti-$k_\mathrm{T}$ $R=0.4$ $|\\eta|<0.4$" ];
plables = [ "$n = 2$", "$n = 3$" ];
# model names : for histonames in ROOT file
modelStr = ["EPOS LHC"]; # "PYTHIA8 Monash2013"];#for legend
#modelStr = ["PYTHIA8 String Shoving $g$ = 3","EPOS LHC"];
#xtitle = ["$p^{\\mathrm{LP}}_\\mathrm{T,min}\\,(\\mathrm{GeV}/c)$","$p^{\\mathrm{Jet}}_\\mathrm{T,min}\\,(\\mathrm{GeV}/c)$"];
#xtitle = ["$p_\\mathrm{T,trig(assoc)}\\,(\\mathrm{GeV}/c)$","$p_\\mathrm{T,trig(assoc)}\\,(\\mathrm{GeV}/c)$"];
xtitle = ["$p_\\mathrm{T,trig}\\,(\\mathrm{GeV}/c)$","$p_\\mathrm{T,trig}\\,(\\mathrm{GeV}/c)$"];
ytitle = ["$V_{n}$"];

# Following two must be added
toptitle = "pp $\\sqrt{s}$ = 13 TeV \n 0--0.1\%"; # need to add on the top
dataDetail = ["$1.6<|\\Delta\\eta|<1.8$ \n 1 $ < p_\\mathrm{T,assoc} < 4 \\,\\mathrm{GeV}/c $"];


plot = JPyPlotRatio.JPyPlotRatio(panels=(nrow,ncol),
	panelsize=(5,5),
	rowBounds=ylimits,  # for nrow
	colBounds=xlimits,  # for ncol
	panelLabel=plables,  # nrowxncol
	ratioBounds=rlimits,# for nrow
#	ratioSystPlot=True,
	disableRatio=[0],
	panelLabelLoc=(0.71,0.89),panelLabelSize=14,panelLabelAlign="left",
	axisLabelSize=14,tickLabelSize=14,legendPanel=0,
	legendLoc=(0.46,0.20),legendSize=14,xlabel={0:xtitle[0],1:xtitle[1]},ylabel=ytitle[0]);

plot.EnableLatex(True); # for publication need fonts via texlive

plotMatrix = np.empty((nrow,ncol),dtype=int);

#plot.GetAxes(0).set_xticks([1.5,2.5,3.5]);


for i in range(0,nrow):
	for j in range(0,ncol):
		index = i*ncol+j; # for each panel 
		#plot.GetAxes(index).set_xticks([1.5,2.5,3.5]);
		plot.GetAxes(index).xaxis.set_ticks_position('both');
		plot.GetAxes(index).yaxis.set_ticks_position('both');
		gr = f.Get("{}".format(histnames[j]));
		datapp = plot.Add(index,gr,**dataTypePlotParams[0],label="pp 13 TeV 0--0.1\%");
		    #, $1.6<|\\Delta\\eta|<1.8$ \n 1 $ < p_\\mathrm{T,assoc} < 4 \\,\\mathrm{GeV}/c $"
		grsyst = f.Get("{}".format(histnamesSyst[j]));
		_,_,_,syst = JPyPlotRatio.TGraphErrorsToNumpy(ROOT.TGraphErrors(grsyst));
		plot.AddSyst(datapp,syst);
		#Loading ATLAS
		grATLAS = f.Get("{}".format(histatlas_stat[j]));
		#data = plot.Add(index,grATLAS,**dataTypePlotParams[1],label="ATLAS, $2.0<|\\Delta\\eta|<5.0$ \n 0.5 $ < p_\\mathrm{T,assoc} < 5 \\,\\mathrm{GeV}/c $");
		#grsystATLAS = f.Get("{}".format(histatlas_syst[j]));
		#_,_,_,syst = JPyPlotRatio.TGraphErrorsToNumpy(ROOT.TGraphErrors(grsystATLAS));
		#plot.AddSyst(data,syst);
		#End of ATLAS
		#Loading pPb
		if(addpPb):
			grpPb = fpPb.Get("{}".format(histpPb_stat[j]));
			grpPb.Print();
			dataPb = plot.Add(index,grpPb,**dataTypePlotParams[2],label="p--Pb 5.02 TeV 0--20\%");
			grsystpPb = fpPb.Get("{}".format(histpPb_syst[j]));
			_,_,_,syst = JPyPlotRatio.TGraphErrorsToNumpy(ROOT.TGraphErrors(grsystpPb));
			plot.AddSyst(dataPb,syst);
			plot.Ratio(dataPb,datapp);
		#End of pPb
		#gr = f.Get("{}".format(histnames[j]));
		#gr.Print();
		#data = plot.Add(index,gr,**dataTypePlotParams[0],label="ALICE, $1.6<|\\Delta\\eta|<1.8$ \n 1 $ < p_\\mathrm{T,assoc} < 4 \\,\\mathrm{GeV}/c $");
		#grsyst = f.Get("{}".format(histnamesSyst[j]));
		#_,_,_,syst = JPyPlotRatio.TGraphErrorsToNumpy(ROOT.TGraphErrors(grsyst));
		#plot.AddSyst(data,syst);

f.Close();

plot.GetPlot().text(0.15,0.80,"ALICE",fontsize=14);
#plot.GetPlot().text(0.15,0.77,"ALICE",fontsize=12);
plot.GetPlot().text(0.54,0.65,dataDetail[0],fontsize=14);
#plot.GetPlot().text(0.16,0.17,dataDetail[1],fontsize=10);

# this is need because of the input histo label setting..
#plot.GetAxes(0).set(xticks=[0.5,1.5,2.5,3.5,4.5,5.5,6.5], xticklabels=["0","3","5","7","9","13","20"]);
#plot.GetAxes(1).set(xticks=[0.5,1.5,2.5,3.5,4.5,5.5], xticklabels=["0","10","20","30","40","50"]);
plot.Plot();
if(addpPb):
	plot.Save("figs/Fig2_vn_pppPb.pdf");
	plot.Save("figs/Fig2_vn_pppPb.png");
else:
    plot.Save("figs/Fig2_vn.pdf")
    plot.Save("figs/Fig2_vn.png");

plot.Show();

