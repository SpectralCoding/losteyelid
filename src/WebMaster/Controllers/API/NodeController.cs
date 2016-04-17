// <copyright file="NodeController.cs" company="SpectralCoding.com">
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
using WebMaster.Models.Node;

// For more information on enabling Web API for empty projects, visit http://go.microsoft.com/fwlink/?LinkID=397860

namespace WebMaster.Controllers.API {
	[Route("api/node")]
	public class NodeController : Controller {
		[FromServices]
		public INodeRepository Nodes { get; set; }

		// GET: api/values
		[HttpGet]
		public IEnumerable<Node> GetAll() {
			return Nodes.GetAll();
		}

		// GET api/values/5
		[HttpGet("{id}", Name = "GetNode")]
		public IActionResult GetById(String id) {
			var item = Nodes.Find(id);
			if (item == null) {
				return HttpNotFound();
			}
			return new ObjectResult(item);
		}

		[HttpPost]
		public IActionResult Create([FromBody] Node item) {
			if (item == null) {
				return HttpBadRequest();
			}
			Nodes.Add(item);
			return CreatedAtRoute("GetNode", new {controller = "Node", id = item.Id}, item);
		}

		[HttpDelete("{id}")]
		public void Delete(String id) {
			Nodes.Remove(id);
		}

		//// PUT api/values/5
		//
		//public void Post([FromBody] String value) { }
		//[HttpPost]

		//// POST api/values
		//[HttpPut("{id}")]
		//public void Put(Int32 id, [FromBody] String value) { }
		//
		//// DELETE api/values/5
		//[HttpDelete("{id}")]
		//public void Delete(Int32 id) { }
	}
}
