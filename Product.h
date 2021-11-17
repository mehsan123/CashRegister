/*
 *    Cashregister project
 * ===========================
 * File Path     : Product.h
 * Author        : M.W.Richardson
 * Date          : 14/01/15
 * Copyright     : (c) 2016 Liverpool Data Research Associates
 */

#ifndef PRODUCT_H
#define PRODUCT_H

#include "Specialoffer.h"

struct Product
{
  LDRA_char_pt name;
  LDRA_uint32_t barcode;
  LDRA_uint32_t unitPrice;
  tSpecialoffer specialOffer;
};

#endif
