// <copyright file="HomeController.cs" company="SpectralCoding.com">
//     Copyright (c) 2016 SpectralCoding
// </copyright>
// <license>
// This file is part of LostEyelid.
// 
// LostEyelid is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// LostEyelid is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
// 
// You should have received a copy of the GNU General Public License
// along with LostEyelid.  If not, see <http://www.gnu.org/licenses/>.
// </license>
// <author>Caesar Kabalan</author>

using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNet.Mvc;

namespace WebMaster.Controllers {
	public class HomeController : Controller {
		public IActionResult Index() {
			return View();
		}

		public IActionResult About() {
			ViewData["Message"] = "Your application description page.";

			return View();
		}

		public IActionResult Contact() {
			ViewData["Message"] = "Your contact page.";

			return View();
		}

		public IActionResult Error() {
			return View();
		}
	}
}
