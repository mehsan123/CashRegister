/*
 *    Cashregister project
 * ===========================
 * File Path     : Userinterface.h
 * Author        : M.W.Richardson
 * Date          : 14/01/15
 * Copyright     : (c) 2016 Liverpool Data Research Associates
 */

#ifndef Userinterface_H
#define Userinterface_H

/*
 * This is the file that can be easily replaced
 * by a different implementation of the printer, display
 * keyboard and barcode reader.
 */

void Userinterface_help(void);
void Userinterface_parse(const LDRA_char_t aChar);
void Userinterface_show(LDRA_const_char_pt displayMsg);
void Userinterface_print(LDRA_const_char_pt printerMsg);

#endif
