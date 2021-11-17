/*
 *    Cashregister project
 * ===========================
 * File Path     : Specialoffer.c
 * Author        : M.W.Richardson
 * Date          : 14/01/15
 * Copyright     : (c) 2016 Liverpool Data Research Associates
 */

#include "Misrac_types.h"
#include "Specialoffer.h"

/*
 * Get the price which depends on which special offer, if any, is used
 */
LDRA_uint32_t Specialoffer_getPrice(const LDRA_uint32_t aQuantity,
    const LDRA_uint32_t aUnitPrice, const tSpecialoffer anOffer)
{
  LDRA_uint32_t price;
  switch (anOffer)
  {
    case BUY_ONE_GET_ONE_FREE:
      price = aUnitPrice * ((aQuantity + 1U) >> 1U);
      break;
    case TEN_PERCENT_OFF:
      price = (aUnitPrice * aQuantity * 9U) / 10U;
      break;
    case THREE_FOR_ONE_EURO:
      price = ((aQuantity / 3U) * 100U) + ((aQuantity % 3U) * aUnitPrice);
      break;
      /* no offer */
    default:
      price = aUnitPrice * aQuantity;
      break;
  }
  return price;
}

