
import numpy as np
import ROOT

import scipy
from scipy import interpolate

import sys
sys.path.append("JPyPlotRatio");
#https://github.com/jaelpark/JPyPlotRatio


import JPyPlotRatio


f = ROOT.TFile("data/Final_Items.root","read");
dataTypePlotParams = [
	{'plotType':'data','color':'k','fmt':'o','markersize':5.0},
	{'plotType':'theory','facecolor':'C0','edgecolor':'C0','alpha':0.5,'linestyle':'solid','linecolor':'C0'},
	{'plotType':'theory','facecolor':'C1','edgecolor':'C1','alpha':0.5,'linestyle':'dotted','linecolor':'C1'},
	{'plotType':'theory','facecolor':'C2','edgecolor':'C2','alpha':0.5,'linestyle':'dashed','linecolor':'C2'},
	{'plotType':'theory','facecolor':'C3','edgecolor':'C3','alpha':0.5,'linestyle':'dashdot','linecolor':'C3'},
];


# define panel/xaxis limits/titles
nrow = 2;
ncol = 2;
xlimits = [
	[(-0.1,7.1),(-0.1,5.1)],
	[(-0.1,4.1),(-0.1,5.1)] ];
ylimits = [(0.04,0.19),(-0.07,0.25)];
rlimits = [(0.,4.5),(0.,4.5)];

# add here the histogram names for each pad
histnames = [
	["v2_lp",	"v2_jet"],
	["v3_lp",  "v3_jet"], ];
histnamesSyst = [
	["v2_0_ALICE_syst",  "v2_1_ALICE_syst"],
	["v3_0_ALICE_syst",  "v3_1_ALICE_syst"], ];
histnamesModels = [
	["v2_0_EPOS",  "v2_1_EPOS"],
	["v3_0_EPOS",  "v3_1_EPOS"], ];

# add labels for each pad
plables = [ "Leading Particle $|\\eta|<0.9$","Jet, anti-$k_\\mathrm{T}$ $R=0.4$ $|\\eta|<0.4$" ,"",""];
# model names : for histonames in ROOT file
modelStr = ["EPOS LHC"]; # "PYTHIA8 Monash2013"];#for legend
#modelStr = ["PYTHIA8 String Shoving $g$ = 3","EPOS LHC"];
xtitle = ["$p^{\\mathrm{LP}}_\\mathrm{T,min}\\,(\\mathrm{GeV}/c)$","$p^{\\mathrm{Jet}}_\\mathrm{T,min}\\,(\\mathrm{GeV}/c)$"];
ytitle = ["$V_{2}$", "$V_{3}$"];

# Following two must be added
toptitle = "pp $\\sqrt{s}$ = 13 TeV, 0--0.1\%"; # need to add on the top
dataDetail = ["$1 < p_\\mathrm{T,trig} < 2\\,\\mathrm{GeV}/c$","$1.6 < |\\Delta\\eta| < 1.8$"];
PanelName = ["LP", "Jet"];

plot = JPyPlotRatio.JPyPlotRatio(panels=(nrow,ncol),
	rowBounds=ylimits,  # for nrow
	colBounds=xlimits[0],  # for ncol
	panelLabel=plables,  # nrowxncol
	ratioBounds=rlimits,# for nrow
	disableRatio=[0,1],
	panelLabelLoc=(0.06,0.54),panelLabelSize=9,panelLabelAlign="left",
	legendPanel=2,
	legendLoc=(0.40,0.64),legendSize=10,xlabel={0:xtitle[0],1:xtitle[1]},
	ylabel={0:ytitle[0],1:ytitle[1]});
plot.EnableLatex(False); # for publication need fonts via texlive

for iobs in range(0,2):
	for j in range(0,ncol):
		index = iobs*ncol+j;
		plot.GetAxes(index).xaxis.set_ticks_position('both');
		plot.GetAxes(index).yaxis.set_ticks_position('both');
		gr = f.Get("{}_stat".format(histnames[iobs][j]));
		gr.Print();

		grsyst = f.Get("{}_syst".format(histnames[iobs][j]));
		_,_,_,syst = JPyPlotRatio.TGraphErrorsToNumpy(ROOT.TGraphErrors(grsyst));

		if index == 2:
			#remove pT_LP > 7 points
			x,y,_,yerr = JPyPlotRatio.TGraphErrorsToNumpy(ROOT.TGraphErrors(gr));
			x,y,yerr = x[:4],y[:4],yerr[:4];
			syst = syst[:4];
			gr = (x,y,yerr);

		data = plot.Add(index,gr,**dataTypePlotParams[0],label="ALICE, $1.6 < |\\Delta\\eta| < 1.8$");
		plot.AddSyst(data,syst);
#			if( iobs==0 ):
#				grModel = f.Get("{}".format(histnamesModels[iobs][j]));
#				data = plot.Add(index,grModel,**dataTypePlotParams[3],label=modelStr[0]);

#			for k in range(0,len(modelStr)):
#				grModel = f.Get("{}".format(histnamesModels[k][j]));
#				model = plot.Add(index,grModel,**dataTypePlotParams[1+k],label=modelStr[k]);
#				if(k>0):
#				plot.Ratio(model,data,dataTypePlotParams[k+1]);
#				plot.Ratio(model,data,style="errorbar"); #Calculate and plot ratio between data and theory
#					plot.Ratio(model,data );


#'''
plot.GetPlot().text(0.15,0.82,toptitle,fontsize=12);
plot.GetPlot().text(0.16,0.78,dataDetail[0],fontsize=11);
#	plot.GetPlot().text(0.14,0.60,dataDetail[1],fontsize=10);
plot.GetPlot().text(0.46,0.80,PanelName[0],fontsize=12);
plot.GetPlot().text(0.84,0.80,PanelName[1],fontsize=12);
plot.GetPlot().text(0.46,0.40,PanelName[0],fontsize=12);
plot.GetPlot().text(0.84,0.40,PanelName[1],fontsize=12);
plot.GetPlot().text(0.54,0.80,"ALICE",fontsize=11);

# this is need because of the input histo label setting..
#if( iobs==0 ):
#	plot.GetAxes(0).set(xticks=[0.5,1.5,2.5,3.5,4.5,5.5,6.5], xticklabels=["Unbiased","3","5","7","9","13","20"]);
#if( iobs==1 ):
#	plot.GetAxes(0).set(xticks=[0.5,1.5,2.5,3.5], xticklabels=["Unbiased","3","5","7"]);
plot.GetAxes(2).set(xticks=[0.5,1.5,2.5,3.5,4.5,5.5,6.5], xticklabels=["Unbiased","3","5","7","9","13","20"]);
#	plot.GetAxes(1).set(xticks=[0.5,1.5,2.5,3.5,4.5,5.5,6.5], xticklabels=["Unbiased","10","20","30","40","50","60"]);
plot.GetAxes(3).set(xticks=[0.5,1.5,2.5,3.5,4.5], xticklabels=["Unbiased","10","20","30","40"]);
cntforaxis=0;
for tick in plot.GetAxes(2).get_xticklabels():
	if( cntforaxis==0 ):
		tick.set(fontsize=8);
		tick.set_rotation(-17)
		cntforaxis += 1;
cntforaxis=0;
for tick in plot.GetAxes(3).get_xticklabels():
	if( cntforaxis==0 ):
		tick.set(fontsize=8);
		tick.set_rotation(-17)
		cntforaxis += 1;
#'''

plot.Plot();
	
plot.Save("figs/Fig4_vn_LP.pdf");
plot.Save("figs/Fig4_vn_LP.png");

plot.Show();

