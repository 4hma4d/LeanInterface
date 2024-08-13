from ...interpreter.interpret import interpret

searchl=["simp"]

def ner(l1, l2):
    return interpret(("".join([x + y for x, y in zip(l1[:-1], l2)]))+l1[-1])[1]

def toLean(text):
    l1 = list(text.split("sorry--<Auto>"))
    print(l1)
    working=["sorry"]*(len(l1)-1)
    found = False
    n=-1
    for l in l1[:-1]:
        n+=1
        l2 = ["sorry"]*(len(l1)-1)
        l2[n]="done"
        nerstart = ner(l1,l2)
        for tac in searchl:
            l2[n]=tac
            nerend= ner(l1,l2)
            if nerstart > nerend:
                working[n]=tac
                print(tac)
                break
            else: continue


    return "".join([x + y for x, y in zip(l1[:-1], working)])+l1[-1]
