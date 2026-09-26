#!/usr/bin/env python3


import argparse
import pandas as pd
import logging


    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pull patron information from Genesis export")
    parser.add_argument("input", help="exported xlsx from Genesis")
    parser.add_argument("--code",help="3 digit school-year code for constructing email address, e.g. 427",required=True)
    parser.add_argument("--output", help="optional path to save the result to. If omitted it prints preview to screen.")

    args = parser.parse_args()

    logging.debug("Opening {0}".format(args.input))
    df = pd.read_excel(args.input)
    logging.debug("Got {0}".format(df.head()))

    # change columns to map to what LibraryCat wants
    mapping_dict = {'Student':'Full name',
                    'ID':'Barcode',
                    'Address':'Address 1',
                    'Email':'Home email'}
    df=df.rename(columns=mapping_dict)

    # add additional columns
    df['State'] = 'NJ'
    zip_dict = {'englishtown':'07726','manalapan':'07726',
                'colts neck':'07722', 'farmingdale':'07727',
                'freehold':'07727',
                'howell':'07731',
                'marlboro':'07746',
                'morganville':'07751'}
    df['Zipcode'] = df['City'].str.lower().map(zip_dict)
    df[['Last', 'firstnames']] = df['Full name'].str.split(',',n=1,expand=True)
    df[['First','Middle']] = df['firstnames'].str.split(n=1,expand=True).fillna('')
    frhsd_email = (
        args.code +
        df['First'].str.strip().str.lower().str[0]+
        df['Last'].str.strip().str.lower()+
        '@frhsd.com'
        )
    df['Email']=frhsd_email

    # add empty columns that LibraryCat wants
    df['Suffix']=''
    df['Address 2']=''
    df['Notes']=''
    
    
    # export to LibraryCat
    result = df[['First','Middle','Last','Suffix',
                 'Barcode','Email','Phone',
                 'Address 1','Address 2','City', 'State', 'Zipcode',
                 'Notes','Home email'
                 ]]
    if args.output is not None:
        result.to_csv(args.output,index=False,encoding='utf-8')
    else:
        print("Produced this")
        pd.set_option('display.max_colwidth', 7)
        print(result)
