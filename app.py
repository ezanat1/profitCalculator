from flask import Flask,render_template,request
import requests
from flask_wtf import Form
from wtforms import StringField,PasswordField,FloatField,SubmitField
from wtforms.validators import InputRequired,Email,Length,AnyOf
from flask_bootstrap import Bootstrap



app = Flask(__name__, template_folder='templates') 
Bootstrap(app)
app.config['SECRET_KEY']='Ekmys@123'


class investmentForm(Form):
    stockSymbol=StringField('Ticket Symbol',validators=[InputRequired(),Length(min=2,max=5,message='Please Enter Correct symbol')])
    allotment=FloatField('Allotment',validators=[InputRequired()])
    finalSharePrice=FloatField('Final Share Price',validators=[InputRequired()])
    sellCommision=FloatField('Sell Commision',validators=[InputRequired()])
    initialSharePrice=FloatField('Initial Share Price',validators=[InputRequired()])
    buyCommission=FloatField('Buy Commission',validators=[InputRequired()])
    taxGain=FloatField('Capital Gain Tax Rate (%)',validators=[InputRequired()])
    submit=SubmitField()
    

def proceeds(allt,fSP):
    return float(allt * fSP)
def cost(pcee,allt,iSP,sCommss,bCommss,taxCP):
    #Calculate cost 
    comissions=sCommss+bCommss
    calc=allt * iSP + comissions
    n=pcee-calc
    taxCP=(15/100) * n
    return float(calc+taxCP)
def returnOnInvestment(netProfit, cost):
    return (100+(netProfit-cost)/cost*100)

def calcBreakEven(iSP, allt, bCommss, sCommss):
    return float((bCommss + sCommss) / allt + iSP)


@app.route("/",methods=['GET','POST'])
def index():
    form=investmentForm()
    if request.method== 'POST' and form.validate():

        #Get form field data
        symb=form.stockSymbol.data
        allotment=form.allotment.data
        sellCommision=form.sellCommision.data
        finalSharePrice=form.finalSharePrice.data
        initialSharePrice=form.initialSharePrice.data
        buyCommission=form.buyCommission.data
        taxGain=form.taxGain.data

        #Calculate Proceeds
        calcProceeds=proceeds(allotment,finalSharePrice)
        #Calculate Net Cost
        calcCost=cost(calcProceeds,allotment,initialSharePrice,sellCommision,buyCommission,taxGain)

        #Raw Profit
        netProfit=calcProceeds-calcCost
        #Breakeven
        calcBreakE=calcBreakEven(initialSharePrice,allotment,buyCommission,sellCommision)
        #Return on investement
        calcReturn=returnOnInvestment(netProfit,calcCost)
        return render_template('price.html',form=form,calcProceeds=calcProceeds,calcCost=calcCost,netProfit=netProfit,calcBreakE=calcBreakE,calcReturn=calcReturn)  
    return render_template('home.html',form=form)

if __name__=='__main__':
    app.run(debug=True)


