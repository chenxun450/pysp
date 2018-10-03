# coding = utf-8

import uiautomator2 as u2

d = u2.connect("172.17.100.15")
print(d.device_info)