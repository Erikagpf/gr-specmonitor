/* -*- c++ -*- */
/* 
 * Copyright 2017 Francisco Paisana.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#include <cassert>
#include <algorithm>
#include <limits>

#ifndef RANGE_UTILS_H_
#define RANGE_UTILS_H_

namespace utils {
  template<typename T>
  struct hist_array_view {
    T* vec;
    int hist_len;
    int d_size;

    hist_array_view() : vec(NULL), hist_len(0) {}

    hist_array_view(T* vec_x, int h_len) :
      vec(vec_x),
      hist_len(h_len),
      d_size(std::numeric_limits<int>::max()) {
    }

    hist_array_view(T* vec_x, int h_len, int siz) :
      vec(vec_x),
      hist_len(h_len),
      d_size(siz) {
    }

    void set(T* vec_x, int h_len, int siz = std::numeric_limits<int>::max()) {
      vec = vec_x;
      hist_len = h_len;
      d_size = siz;
    }

    inline T& operator[](int i) {
      assert(i>=-hist_len && i <= d_size);
      return vec[i+hist_len];
    }

    inline const T& operator[](int i) const {
      assert(i>=-hist_len && i <= d_size);
      return vec[i+hist_len];
    }

    inline void advance(int siz) {
      std::copy(&vec[siz], &vec[siz+hist_len], &vec[0]);
    }
  };
}

#endif
