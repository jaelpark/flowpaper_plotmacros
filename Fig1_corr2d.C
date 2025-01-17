void Fig1_corr2d(){
 TFile* fpp  = new TFile("data/Corr2d_figures_pp.root","read");
 TFile* fpPb = new TFile("data/Corr2d_figures_pPb.root","read");

 TH2D* h2D_pp_high = (TH2D*)fpp->Get("hC_5_0_0_2_11");
 TH2D* h2D_pp_low  = (TH2D*)fpp->Get("hC_0_0_0_4_11");
 TH2D* h2D_pp_sub  = (TH2D*)fpp->Get("hCSUB_0_0_0_11");

 TH2D* h2D_pPb_high = (TH2D*)fpPb->Get("hC_1_0_0_0_2");
 TH2D* h2D_pPb_low  = (TH2D*)fpPb->Get("hC_1_0_0_6_2");
 TH2D* h2D_pPb_sub  = (TH2D*)fpPb->Get("hCSUB_1_0_2");

 TH2D* hStyle[6];
 hStyle[0] = (TH2D*)h2D_pp_high;
 hStyle[1] = (TH2D*)h2D_pp_low;
 hStyle[2] = (TH2D*)h2D_pp_sub;
 hStyle[3] = (TH2D*)h2D_pPb_high;
 hStyle[4] = (TH2D*)h2D_pPb_low;
 hStyle[5] = (TH2D*)h2D_pPb_sub;

 for(int i=0;i<6;i++){
	hStyle[i]->GetXaxis()->SetTitle( hStyle[0]->GetXaxis()->GetTitle() );
	hStyle[i]->GetYaxis()->SetTitle( hStyle[0]->GetYaxis()->GetTitle() );
	hStyle[i]->GetZaxis()->SetTitle( hStyle[0]->GetZaxis()->GetTitle() );

	hStyle[i]->GetXaxis()->SetTitleFont(43);
	hStyle[i]->GetXaxis()->SetLabelFont(43);
	hStyle[i]->GetYaxis()->SetTitleFont(43);
	hStyle[i]->GetYaxis()->SetLabelFont(43);
	hStyle[i]->GetZaxis()->SetTitleFont(43);
	hStyle[i]->GetZaxis()->SetLabelFont(43);

	hStyle[i]->GetXaxis()->SetTitleSize(32);
	hStyle[i]->GetYaxis()->SetTitleSize(32);
	hStyle[i]->GetZaxis()->SetTitleSize(32);
	hStyle[i]->GetXaxis()->SetLabelSize(28);
	hStyle[i]->GetYaxis()->SetLabelSize(28);
	hStyle[i]->GetZaxis()->SetLabelSize(28);

	hStyle[i]->GetZaxis()->SetNdivisions(505);	
	hStyle[i]->GetZaxis()->SetTitleOffset(1.33);

 }

 const char description[6][100] = {
	"0#font[122]{-}0.1%, V0M",
	"60#font[122]{-}100%, V0M",
	"(0#font[122]{-}0.1%) - #it{F}(60#font[122]{-}100%), V0M",
        "0#font[122]{-}5%, V0A",
        "60#font[122]{-}100%, V0A",
        "(0#font[122]{-}5%) - #it{F}(60#font[122]{-}100%), V0A" };
 const char savename[6][100] = {
	"ppHigh",
	"ppLow",
	"ppSub",
	"pPbHigh",
	"pPbLow",
	"pPbSub" };


 TCanvas* c = new TCanvas("c","c",800,700);
 gPad->SetLeftMargin(0.15);
 gPad->SetBottomMargin(0.09);
 gPad->SetRightMargin(0.03);
 gPad->SetTopMargin(0.03);
 gStyle->SetOptStat(0);
 gPad->SetTicks();

 TLegend* leg = new TLegend(0.01,0.93,0.2,0.99);
 leg->SetFillStyle(0);
 leg->SetLineWidth(0.0);
 leg->SetTextSize(32);
 leg->SetTextFont(43);

 for(int i=0;i<6;i++){
	leg->Clear();
	hStyle[i]->Draw("surf1");
	leg->AddEntry( (TObject*)0, description[i], "");
	leg->Draw();

	c->SaveAs(Form("figs/Fig1_%s.pdf",savename[i]));
	c->SaveAs(Form("figs/Fig1_%s.jpg",savename[i]));
 }


}
