
def dialsNnums(gui,Dials,Nums):
    
    if len(Dials)==len(Nums):
        for i in xrange(len(Dials)):
            Dials[i].valueChanged.connect(Nums[i].setValue)
            Nums[i].valueChanged.connect(Dials[i].setValue)
            
    else:
        raise ValueError('Length mismatch between Dials and Nums')