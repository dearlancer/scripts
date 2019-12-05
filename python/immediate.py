import sys

# 循环右移
def ror(val, r_bits, max_bits):
  return ((val & (2**max_bits-1)) >> r_bits % max_bits) | (val << (max_bits-(r_bits % max_bits)) & (2**max_bits-1))

max_bits = 32

input = int(input("请输入待检测的数字: "))

print()
# 判断立即数是否可用的公式v=n ror 2*r, n的范围:[1,255] r的范围:[0,15] ror代表循环右移
for n in range(1, 256):

    for i in range(0, 31, 2):

        rotated = ror(n, i, max_bits)

        if(rotated == input):
            print("%i 是可用的立即数." % input)
            print("%i ror %x --> %s" % (n, int(str(i), 16), rotated))
            print()
            sys.exit()

else:
    print("Sorry, %i 不是可用的立即数，需要拆分使用." % input)


