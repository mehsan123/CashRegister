/*
 *    Sourcery_CodeBench_ARM_Cashregister project
 * =================================================
 * File Path     : Countedproduct.h
 * Author        : M.W.Richardson
 * Date          : 14/01/15
 * Copyright     : (c) 2015 Liverpool Data Research Associates
 */

#ifndef COUNTEDPRODUCT_H
#define COUNTEDPRODUCT_H

#include "Product.h"

struct CountedProduct
{
  const struct Product* itsProduct;
  LDRA_uint32_t count;
};

#endif
