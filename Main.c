/*
 *    Cashregister project
 * ===========================
 * File Path     : Main.c
 * Author        : M.W.Richardson
 * Date          : 14/01/15
 * Copyright     : (c) 2016 Liverpool Data Research Associates
 */

/*LDRA_INSPECTED 130 S: MISRA-C 2012/AMD1 Required - This include was added so that the code can print something out when it runs */
#include <stdio.h>

#include "Misrac_types.h"
#include "Userinterface.h"

/*LDRA_HEADER_END */

/* 
 * Simple main that loops 
 * until the character 'q' is pressed
 * Then it exits
 */
LDRA_int32_t main(void) 
{
  LDRA_char_t theChar = '0';

  (void) printf("LDRA MISRA C:2012 Cash Register\n");
  Userinterface_help();

  /* Parse characters received from the keyboard */
  while (theChar != 'q')
  {
    theChar = (LDRA_char_t) getchar();
    Userinterface_parse(theChar);    
  }
  return 1;
}
