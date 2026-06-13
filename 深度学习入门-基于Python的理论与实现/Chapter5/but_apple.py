from layer_naive import *

apple=100
apple_num=2
tax=1.1

mul_apple_layer=MulLayer()
mul_tax_layer=MulLayer()

#前向传播
apple_price=mul_apple_layer.forward(apple,apple_num) #第一层前向传播 x=apple=100,y=apple_num=2
price=mul_tax_layer.forward(apple_price,tax) #第二层前向传播 x=apple_price=200,y=tax=1.1

#反向传播
dprice=1
dapple_price,dtax=mul_tax_layer.backward(dprice) #dx=dprice*y=1.1 dy=dprice*x=200
dapple,dapple_num= mul_apple_layer.backward(dapple_price)  #dx=dapple_price*y=2.2 dy=dapple_price*x=110

print("price:", int(price))
print("dApple:", dapple)
print("dApple_num:", int(dapple_num))
print("dTax:", dtax)
