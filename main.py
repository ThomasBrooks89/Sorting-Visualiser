import pygame

a = 36
b = 42

gcf = 1
for i in range(1, min(a, b) + 1):
    if a % i == 0 and b % i == 0:
        gcf = i
print(gcf)