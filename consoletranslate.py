import googletrans
from googletrans import Translator
from threading import Thread

class Translate:
    def __init__(self) -> None:
        self.textToTranslate = ""
        self.AllMultiLangList = []
        self.SetMultiLang()
        #self.GetAllLanguages()
        
    def GetAllLanguages(self):
        print((self.AllMultiLangList))
    
    def SetMultiLang(self):
            index = 0
            for i in googletrans.LANGUAGES:
                self.AllMultiLangList.insert(index,i+" = "+str( googletrans.LANGUAGES.get(i) ))
                index+=1
        
    def MultiTranslate(self):
            self.textToTranslate = input("Text to translate: ")
            translator = Translator()
            for lang in ( self.AllMultiLangList ):
                t = Thread(target = lambda: print( (translator.translate(self.textToTranslate,src="pl",dest=lang.split()[0])).text ) )
                t.start()    
trans = Translate()
trans.MultiTranslate()