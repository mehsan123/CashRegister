/*
 *    Cashregister project
 * ===========================
 * File Path     : Productdatabase.c
 * Author        : M.W.Richardson
 * Date          : 14/01/15
 * Copyright     : (c) 2016 Liverpool Data Research Associates
 */

#include "Misrac_types.h"
#include "Countedproduct.h"
#include "Productdatabase.h"

#define NULL_POINTER ((void *)0)

static struct Product ProductList[MAX_PRODUCTS] = { 
  { "Coconuts", 12345U, 180U, TEN_PERCENT_OFF }, 
  { "Lychees", 12346U, 250U, NO_OFFER }, 
  { "Kiwis", 12347U, 50U, THREE_FOR_ONE_EURO }, 
  { "Pears", 12348U, 100U, NO_OFFER }, 
  { "Pomegranates", 12349U, 199U, BUY_ONE_GET_ONE_FREE }, 
  { "Watermelons", 12350U, 350U, NO_OFFER } 
};

static struct CountedProduct CountedProductList[MAX_PRODUCTS] = { 
  { &ProductList[0], 0U }, { &ProductList[1], 0U }, { &ProductList[2], 0U }, 
  { &ProductList[3], 0U }, { &ProductList[4], 0U }, { &ProductList[5], 0U }
};

/*LDRA_HEADER_END */

/*
 * Get the product given the barcode
 * If no product exists, then return null
 */
const struct Product* Productdatabase_getProduct(const LDRA_uint32_t bCode)
{
  LDRA_uint32_t pIter = 0U;
  /*LDRA_INSPECTED 8 D: MISRA C 2012/AMD1 R2.2 Required - No simple way to avoid a DD anomaly */
  const struct Product* theProduct = NULL_POINTER;

  while (pIter < MAX_PRODUCTS)
  {
    if (ProductList[pIter].barcode == bCode)
    {
      theProduct = &ProductList[pIter];
      pIter = MAX_PRODUCTS; /* found it so exit loop */
    }
    else
    {
      pIter++;
    }
  }
  /*LDRA_INSPECTED 71 S: MISRA C 2012/AMD1 R18.6 Required - Returned pointer is ok */
  return theProduct;
}

/*
 * Get the counted product given a product
 * If no counted product exists, then return null
 */
struct CountedProduct* Productdatabase_getCountedProduct(
    const struct Product* bProduct)
{
  LDRA_uint32_t cpIter;
  /*LDRA_INSPECTED 8 D: MISRA C 2012/AMD1 R2.2 Required - No simple way to avoid a DD anomaly */
  struct CountedProduct* theCountedProduct = NULL_POINTER;

  if (bProduct != NULL_POINTER)
  {
    cpIter = 0U;
    while (cpIter < MAX_PRODUCTS)
    {
      if (CountedProductList[cpIter].itsProduct->barcode == bProduct->barcode)
      {
        theCountedProduct = &CountedProductList[cpIter];
        cpIter = MAX_PRODUCTS; /* found it so exit loop */
      }
      else
      {
        cpIter++;
      }
    }
  }
  /*LDRA_INSPECTED 71 S: MISRA C 2012/AMD1 R18.6 Required - Returned pointer is ok */
  return theCountedProduct;
}

/*
 * Get the counted product given an index
 * If index is out of range, then return null
 */
struct CountedProduct* Productdatabase_getSpecificCountedProduct(
    const LDRA_uint32_t anIndex)
{
  struct CountedProduct* theCP;
  if (anIndex < MAX_PRODUCTS)
  {
    theCP = &CountedProductList[anIndex];
  }
  else
  {
    theCP = NULL_POINTER;
  }
  /*LDRA_INSPECTED 71 S: MISRA C 2012/AMD1 R18.6 Required - Returned pointer is ok */
  return theCP;
}

/*
 * Initalise count of all counted products to zero
 */
void Productdatabase_resetCountedProducts(void)
{
  LDRA_uint32_t iCP;

  for (iCP = 0U; iCP < MAX_PRODUCTS; iCP++)
  {
    CountedProductList[iCP].count = 0U;
  }
}

