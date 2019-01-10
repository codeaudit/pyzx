# PyZX - Python library for quantum circuit rewriting 
#        and optimisation using the ZX-calculus
# Copyright (C) 2018 - Aleks Kissinger and John van de Wetering

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
This file contains rewrite rules for ZX-graphs based on the ZX-calculus.

The current rewrites are based on:

- Spider fusion.
- The bialgebra equation.
- Local Complementation.
- Pivoting.
- Removing of identities.

Each of these rewrite rules consists of three methods:

- ``match_*`` finds a single match of the rule in a graph.
- ``match_*_parallel`` finds as many non-overlapping matches as possible.
- The final method takes a list of matches produced by these methods and returns
  a 4-tuple ``(edge_table, verts_to_remove, edges_to_remove, check_for_isolated_vertices)``.
  ``edge_table`` should be fed to :meth:`~graph.base.BaseGraph.add_edge_table`, 
  ``verts_to_remove`` to :meth:`~graph.base.BaseGraph.remove_vertices` (and similarly for ``edges_to_remove``).
  If ``check_for_isolated_vertices`` is ``True``, then 
  :meth:`~graph.base.BaseGraph.remove_isolated_vertices`
  should be called.

These rewrite rules are used in the simplification procedures of :mod:`simplify`.
"""

from fractions import Fraction
import itertools


def apply_rule(g, rewrite, m, check_isolated_vertices=True):
    etab, rem_verts, rem_edges, check_isolated_vertices = rewrite(g, m)
    g.add_edge_table(etab)
    g.remove_edges(rem_edges)
    g.remove_vertices(rem_verts)
    if check_isolated_vertices: g.remove_isolated_vertices()


def match_bialg(g):
    """Does the same as :func:`match_bialg_parallel` but with ``num=1``."""
    types = g.types()
    for e in g.edges():
        v0, v1 = g.edge_st(e)
        v0t = types[v0]
        v1t = types[v1]
        if ((v0t == 1 and v1t == 2) or (v0t == 2 and v1t == 1)):
            v0n = [n for n in g.neighbours(v0) if not n == v1]
            v1n = [n for n in g.neighbours(v1) if not n == v0]
            if (
                all([types[n] == v1t for n in v0n]) and
                all([types[n] == v0t for n in v1n])):
                return [[v0,v1,v0n,v1n]]
    return []


#TODO: make it be hadamard edge aware
def match_bialg_parallel(g, matchf=None, num=-1):
    """Finds noninteracting matchings of the bialgebra rule.
    
    :param g: An instance of a ZX-graph.
    :param matchf: An optional filtering function for candidate edge, should
       return True if a edge should considered as a match. Passing None will
       consider all edges.
    :param num: Maximal amount of matchings to find. If -1 (the default)
       tries to find as many as possible.
    :param edgelist: List of edges to consider. If -1 (the default), looks 
       at all edges.
    :rtype: List of 4-tuples ``(v1, v2, neighbours_of_v1,neighbours_of_v2)``
    """
    if matchf != None: candidates = set([e for e in g.edges() if matchf(e)])
    else: candidates = g.edge_set()
    types = g.types()
    
    i = 0
    m = []
    while (num == -1 or i < num) and len(candidates) > 0:
        v0, v1 = g.edge_st(candidates.pop())
        v0t = types[v0]
        v1t = types[v1]
        if ((v0t == 1 and v1t == 2) or (v0t == 2 and v1t == 1)):
            v0n = [n for n in g.neighbours(v0) if not n == v1]
            v1n = [n for n in g.neighbours(v1) if not n == v0]
            if (
                all([types[n] == v1t for n in v0n]) and
                all([types[n] == v0t for n in v1n])):
                i += 1
                for v in v0n:
                    for c in g.incident_edges(v): candidates.discard(c)
                for v in v1n:
                    for c in g.incident_edges(v): candidates.discard(c)
                m.append([v0,v1,v0n,v1n])
    return m


def bialg(g, matches):
    """Performs a certain type of bialgebra rewrite given matchings supplied by
    ``match_bialg(_parallel)``."""
    rem_verts = []
    etab = dict()
    for m in matches:
        rem_verts.append(m[0])
        rem_verts.append(m[1])
        es = [(i,j) if i < j else (j,i) for i in m[2] for j in m[3]]
        for e in es:
            if e in etab: etab[e][0] += 1
            else: etab[e] = [1,0]
    
    return (etab, rem_verts, [], True)

def match_spider(g):
    """Does the same as :func:`match_spider_parallel` but with ``num=1``."""
    for e in g.edges():
        if g.edge_type(e) != 1: continue
        v0, v1 = g.edge_st(e)
        if (g.type(v0) == g.type(v1)):
            return [[v0,v1]]
    return []

def match_spider_parallel(g, matchf=None, num=-1):
    """Finds noninteracting matchings of the spider fusion rule.
    
    :param g: An instance of a ZX-graph.
    :param matchf: An optional filtering function for candidate edge, should
       return True if a edge should considered as a match. Passing None will
       consider all edges.
    :param num: Maximal amount of matchings to find. If -1 (the default)
       tries to find as many as possible.
    :rtype: List of 2-tuples ``(v1, v2)``
    """
    if matchf != None: candidates = set([e for e in g.edges() if matchf(e)])
    else: candidates = g.edge_set()
    types = g.types()
    
    i = 0
    m = []
    while (num == -1 or i < num) and len(candidates) > 0:
        e = candidates.pop()
        if g.edge_type(e) != 1: continue
        v0, v1 = g.edge_st(e)
        v0t = types[v0]
        v1t = types[v1]
        if (v0t == v1t and v0t!=0):
                i += 1
                for v in g.neighbours(v0):
                    for c in g.incident_edges(v): candidates.discard(c)
                for v in g.neighbours(v1):
                    for c in g.incident_edges(v): candidates.discard(c)
                m.append([v0,v1])
    return m

def spider(g, matches):
    '''Performs spider fusion given a list of matchings from ``match_spider(_parallel)``
    '''
    rem_verts = []
    etab = dict()
    types = g.types()

    for m in matches:
        v0 = m[0]
        g.set_phase(v0, g.phase(v0) + g.phase(m[1]))

        # always delete the second vertex in the match
        rem_verts.append(m[1])

        # edges from the second vertex are transferred to the first
        for v1 in g.neighbours(m[1]):
            if v0 == v1: continue
            e = (v0,v1)
            if e not in etab: etab[e] = [0,0]
            etab[e][g.edge_type((m[1],v1))-1] += 1
    
    return (etab, rem_verts, [], True)

def unspider(g, m, qubit=-1, row=-1):
    """Undoes a single spider fusion, given a match ``m``. A match is a list with 3
    elements given by::

      m[0] : a vertex to unspider
      m[1] : the neighbours of the new node, which should be a subset of the
             neighbours of m[0]
      m[2] : the phase of the new node. If omitted, the new node gets all of the phase of m[0]

    Returns the index of the new node. Optional parameters ``qubit`` and ``row`` can be used
    to position the new node. If they are omitted, they are set as the same as the old node.
    """
    v = g.add_vertex(ty=g.type(m[0]))
    g.set_qubit(v, qubit if qubit != -1 else g.qubit(m[0]))
    g.set_row(v, row if row != -1 else g.row(m[0]))

    g.add_edge((m[0], v))
    for n in m[1]:
        e = g.edge(m[0],n)
        g.add_edge((v,n), edgetype=g.edge_type(e))
        g.remove_edge(e)
    if len(m) >= 3:
        g.add_phase(v, m[2])
        g.add_phase(m[0], Fraction(0) - m[2])
    else:
        g.set_phase(v, g.phase(m[0]))
        g.set_phase(m[0], 0)
    return v


# TODO: optimise for single-match case
def match_pivot(g):
    """Does the same as :func:`match_pivot_parallel` but with ``num=1``."""
    return match_pivot_parallel(g, num=1, check_edge_types=True)


def match_pivot_parallel(g, matchf=None, num=-1, check_edge_types=False):
    """Finds noninteracting matchings of the pivot rule.
    
    :param g: An instance of a ZX-graph.
    :param num: Maximal amount of matchings to find. If -1 (the default)
       tries to find as many as possible.
    :param check_edge_types: Whether the method has to check if all the edges involved
       are of the correct type (Hadamard edges).
    :param matchf: An optional filtering function for candidate edge, should
       return True if a edge should considered as a match. Passing None will
       consider all edges.
    :rtype: List of 4-tuples. See :func:`pivot` for the details.
    """
    if matchf != None: candidates = set([e for e in g.edges() if matchf(e)])
    else: candidates = g.edge_set()
    types = g.types()
    phases = g.phases()
    
    i = 0
    m = []
    while (num == -1 or i < num) and len(candidates) > 0:
        e = candidates.pop()
        if not check_edge_types and g.edge_type(e) != 2: continue
        v0, v1 = g.edge_st(e)

        if not (types[v0] == 1 and types[v1] == 1): continue

        v0a = phases[v0]
        v1a = phases[v1]
        if not ((v0a in (0,1)) and (v1a in (0,1))): continue

        invalid_edge = False

        v0n = list(g.neighbours(v0))
        v0b = []
        for n in v0n:
            #if g.phase(n).denominator > 2:
            #    invalid_edge = True
            #    break
            et = g.edge_type(g.edge(v0,n))
            if types[n] == 1 and et == 2: pass
            elif types[n] == 0: v0b.append(n)
            else:
                invalid_edge = True
                break

        if invalid_edge: continue

        v1n = list(g.neighbours(v1))
        v1b = []
        for n in v1n:
            #if g.phase(n).denominator > 2:
            #    invalid_edge = True
            #    break
            et = g.edge_type(g.edge(v1,n))
            if types[n] == 1 and et == 2: pass
            elif types[n] == 0: v1b.append(n)
            else:
                invalid_edge = True
                break

        if invalid_edge: continue
        if not (len(v0b) + len(v1b) <= 1): continue

        i += 1
        for v in v0n:
            for c in g.incident_edges(v): candidates.discard(c)
        for v in v1n:
            for c in g.incident_edges(v): candidates.discard(c)
        #n0 = list(v0n - v1n)
        #n01 = list(v0n & v1n)
        #n1 = list(v1n - v0n)
        b0 = list(v0b)
        b1 = list(v1b)
        m.append([v0,v1,b0,b1])
    return m

def match_pivot_gadget(g, matchf=None, num=-1):
    """Like :func:`match_pivot_parallel`, but except for pairings of
    Pauli vertices, it looks for a pair of an interior Pauli vertex and an
    interior non-Clifford vertex in order to gadgetize the non-Clifford vertex."""
    if matchf != None: candidates = set([e for e in g.edges() if matchf(e)])
    else: candidates = g.edge_set()
    types = g.types()
    phases = g.phases()
    rs = g.rows()
    
    edge_list = []
    
    
    i = 0
    m = []
    
    while (num == -1 or i < num) and len(candidates) > 0:
        e = candidates.pop()
        v0, v1 = g.edge_st(e)

        if not (types[v0] == 1 and types[v1] == 1): continue

        v0a = phases[v0]
        v1a = phases[v1]
        
        if v0a not in (0,1):
            if v1a in (0,1):
                t = v0
                v0 = v1
                v1 = t
                t = v0a
                v0a = v1a
                v1a = t
            else: continue
        elif v1a in (0,1): continue
        # Now v0 has a Pauli phase and v1 has a non-Pauli phase
        
        v0n = list(g.neighbours(v0))
        v1n = list(g.neighbours(v1))
        if len(v0n) == 1 or len(v1n) == 1: continue # one of them is a phase gadget
        bad_match = False
        discard_edges = []
        for l in (v0n, v1n):
            for n in l:
                if types[n] != 1: 
                    bad_match = True
                    break
                ne = list(g.incident_edges(n))
                if len(ne) == 1: # v0 or v1 is a phase gadget
                    bad_match = True
                    break
                discard_edges.extend(ne)
            if bad_match: break
        if bad_match: continue
                
        if any(types[w]!=1 for w in v0n): continue
        if any(types[w]!=1 for w in v1n): continue
        # Both v0 and v1 are interior
        
        v = g.add_vertex(1,-2,rs[v0],v1a)
        g.set_phase(v1, 0)
        g.set_qubit(v0,-1)
        edge_list.append((v,v1) if v<v1 else (v1,v))
        
        m.append([v0,v1,[],[v]])
        i += 1
        for c in discard_edges: candidates.discard(c)
    g.add_edges(edge_list,1)
    return m

def pivot(g, matches):
    """Perform a pivoting rewrite, given a list of matches as returned by
    ``match_pivot(_parallel)``. A match is itself a list where:

    ``m[0]`` : first vertex in pivot.
    ``m[1]`` : second vertex in pivot.
    ``m[2]`` : list of zero or one boundaries adjacent to ``m[0]``.
    ``m[3]`` : list of zero or one boundaries adjacent to ``m[1]``.
    """
    rem_verts = []
    rem_edges = []
    etab = dict()
    for m in matches:
        # compute:
        #  n[0] <- non-boundary neighbours of m[0] only
        #  n[1] <- non-boundary neighbours of m[1] only
        #  n[2] <- non-boundary neighbours of m[0] and m[1]
        n = [set(g.neighbours(m[0])), set(g.neighbours(m[1]))]
        for i in range(2):
            n[i].remove(m[1-i])
            if len(m[i+2]) == 1: n[i].remove(m[i+2][0])
        n.append(n[0] & n[1])
        n[0] = n[0] - n[2]
        n[1] = n[1] - n[2]
        es = ([(s,t) if s < t else (t,s) for s in n[0] for t in n[1]] +
              [(s,t) if s < t else (t,s) for s in n[1] for t in n[2]] +
              [(s,t) if s < t else (t,s) for s in n[0] for t in n[2]])
        
        for v in n[2]: g.add_to_phase(v, 1)

        for i in range(2):
            # if m[i] has a phase, it will get copied on to the neighbours of m[1-i]:
            a = g.phase(m[i])
            for v in n[1-i]: g.add_to_phase(v, a)
            for v in n[2]: g.add_to_phase(v, a)


            if not m[i+2]:
                # if there is no boundary, the other vertex is destroyed
                rem_verts.append(m[1-i])
            else:
                # if there is a boundary, toggle whether it is an h-edge or a normal edge
                # and point it at the other vertex
                e = g.edge(m[i], m[i+2][0])
                new_e = (m[1-i], m[i+2][0])
                if new_e[0] > new_e[1]: new_e = (new_e[1],new_e[0])
                ne,nhe = etab.get(new_e, (0,0))
                if g.edge_type(e) == 1: nhe += 1
                elif g.edge_type(e) == 2: ne += 1
                etab[new_e] = (ne,nhe)
                rem_edges.append(e)
                


        for e in es:
            nhe = etab.get(e, (0,0))[1]
            etab[e] = (0,nhe+1)

    return (etab, rem_verts, rem_edges, True)

def match_lcomp(g):
    """Same as :func:`match_lcomp_parallel`, but with ``num=1``"""
    return match_lcomp_parallel(g, num=1, check_edge_types=True)

def match_lcomp_parallel(g, vertexf=None, num=-1, check_edge_types=False):
    """Finds noninteracting matchings of the local complementation rule.
    
    :param g: An instance of a ZX-graph.
    :param num: Maximal amount of matchings to find. If -1 (the default)
       tries to find as many as possible.
    :param check_edge_types: Whether the method has to check if all the edges involved
       are of the correct type (Hadamard edges).
    :param vertexf: An optional filtering function for candidate vertices, should
       return True if a vertex should be considered as a match. Passing None will
       consider all vertices.
    :rtype: List of 2-tuples ``(vertex, neighbours)``.
    """
    if vertexf != None: candidates = set([v for v in g.vertices() if vertexf(v)])
    else: candidates = g.vertex_set()
    types = g.types()
    phases = g.phases()
    
    i = 0
    m = []
    while (num == -1 or i < num) and len(candidates) > 0:
        v = candidates.pop()
        vt = types[v]
        va = g.phase(v)
        
        if not (va == Fraction(1,2) or va == Fraction(3,2)): continue

        if check_edge_types and not (
            all(g.edge_type(e) == 2 for e in g.incident_edges(v))
            ): continue
                
        vn = list(g.neighbours(v))

        if not all(types[n] == vt for n in vn): continue # and phases[n].denominator <= 2

        for n in vn: candidates.discard(n)
        m.append([v,vn])
    return m

def lcomp(g, matches):
    """Performs a local complementation based rewrite rule on the given graph with the
    given ``matches`` returned from ``match_lcomp(_parallel)``. See *insert paper here* 
    for more details on the rewrite"""
    etab = dict()
    rem = []
    for m in matches:
        a = g.phase(m[0])
        rem.append(m[0])
        for i in range(len(m[1])):
            g.add_to_phase(m[1][i], -a)
            for j in range(i+1, len(m[1])):
                e = (m[1][i],m[1][j])
                if (e[0] > e[1]): e = (e[1],e[0])
                he = etab.get(e, (0,0))[1]
                etab[e] = (0, he+1)

    return (etab, rem, [], False)


def match_ids(g):
    """Finds a single identity node. See :func:`match_ids_parallel`."""
    return match_ids_parallel(g, num=1)

def match_ids_parallel(g, vertexf=None, num=-1):
    """Finds noninteracting identity nodes.
    
    :param g: An instance of a ZX-graph.
    :param num: Maximal amount of matchings to find. If -1 (the default)
       tries to find as many as possible.
    :param vertexf: An optional filtering function for candidate vertices, should
       return True if a vertex should be considered as a match. Passing None will
       consider all vertices.
    :rtype: List of 4-tuples ``(identity_vertex, neighbour1, neighbour2, edge_type)``.
    """
    if vertexf != None: candidates = set([v for v in g.vertices() if vertexf(v)])
    else: candidates = g.vertex_set()
    types = g.types()
    phases = g.phases()

    i = 0
    m = []

    while (num == -1 or i < num) and len(candidates) > 0:
        v = candidates.pop()
        if phases[v] != 0: continue
        neigh = g.neighbours(v)
        if len(neigh) != 2: continue
        v0, v1 = neigh
        candidates.discard(v0)
        candidates.discard(v1)
        if g.edge_type((v,v0)) != g.edge_type((v,v1)): #exactly one of them is a hadamard edge
            m.append((v,v0,v1,2))
        else: m.append((v,v0,v1,1))
        i += 1
    return m

def remove_ids(g, matches):
    """Given the output of ``match_ids(_parallel)``, returns a list of edges to add,
    and vertices to remove."""
    etab = dict()
    rem = []
    for m in matches:
        rem.append(m[0])
        e = (m[1],m[2])
        if not e in etab: etab[e] = [0,0]
        etab[e][m[3]-1] += 1
    return (etab, rem, [], False)
    


def match_phase_gadgets(g):
    phases = g.phases()

    parities = dict()
    gadgets = dict()
    for v in g.vertices():
        if phases[v] != 0 and phases[v].denominator > 2 and len(list(g.neighbours(v)))==1:
            n = list(g.neighbours(v))[0]
            gadgets[n] = v
            par = frozenset(set(g.neighbours(n)).difference({v}))
            if par in parities: parities[par].append(n)
            else: parities[par] = [n]

    m = []
    for par, gad in parities.items():
        if len(gad) == 1: 
            n = gad[0]
            v = gadgets[n]
            if phases[n] != 0:
                m.append((v,n,-phases[v],[],[]))
        else:
            totphase = sum((1 if phases[n]==0 else -1)*phases[gadgets[n]] for n in gad)%2
            n = gad.pop()
            v = gadgets[n]
            m.append((v,n,totphase, gad, [gadgets[n] for n in gad]))

    return m

def merge_phase_gadgets(g, matches):
    rem = []
    for v, n, phase, othergadgets, othertargets in matches:
        g.set_phase(v, phase)
        g.set_phase(n, 0)
        rem.extend(othergadgets)
        rem.extend(othertargets)
    return ({}, rem, [], False)



def match_gadgets_phasepoly(g):
    targets = {}
    gadgets = {}
    for v in g.vertices():
        if v not in g.inputs and v not in g.outputs and len(list(g.neighbours(v)))==1:
            if g.phase(v) != 0 and g.phase(v).denominator != 4: continue
            n = list(g.neighbours(v))[0]
            tgts = frozenset(set(g.neighbours(n)).difference({v}))
            if len(tgts)>4: continue
            gadgets[tgts] = (n,v)
            for t in tgts:
                if t in targets: targets[t].add(tgts)
                else: targets[t] = {tgts}
        if g.phase(v) != 0 and g.phase(v).denominator == 4:
            if v in targets: targets[v].add(frozenset([v]))
            else: targets[v] = {frozenset([v])}
    targets = {t:s for t,s in targets.items() if len(s)>1}
    matches = {}

    for v1,t1 in targets.items():
        s = t1.difference(frozenset([v1]))
        if len(s) == 1:
            c = s.pop()
            if any(len(targets[v2])==2 for v2 in c): continue
        s = t1.difference({frozenset({v1})})
        for c in [d for d in s if not any(d.issuperset(e) for e in s if e!=d)]:
            if not all(v2 in targets for v2 in c): continue
            if any(v2<v1 for v2 in c): continue
            a = set()
            for t in c: a.update([i for s in targets[t] for i in s if i in targets])
            for group in itertools.combinations(a.difference(c),4-len(c)):
                group = list(group)+list(c)
                a = set()
                for t in group: a.update([s for s in targets[t] if s.issubset(group)])
                if len(a)>7:
                    matches[frozenset(group)] = a

    m = []
    taken = set()
    for group, gad in sorted(matches.items(), key=lambda a: len(a[1]), reverse=True):
        if taken.intersection(group): continue
        m.append((list(group), {s:(gadgets[s] if len(s)>1 else list(s)[0]) for s in gad}))
        taken.update(group)

    return m


def apply_gadget_phasepoly(g, matches):
    rs = g.rows()
    phases = g.phases()
    for group, gadgets in matches:
        for i in range(4):
            v1 = group[i]
            g.add_to_phase(v1, Fraction(5,4))
            
            for j in range(i+1,4):
                v2 = group[j]
                f = frozenset({v1,v2})
                if f in gadgets:
                    n,v = gadgets[f]
                    phase = phases[v]
                    if phases[n]:
                        phase = -phase
                        g.set_phase(n,0)
                else:
                    n = g.add_vertex(1,-1, rs[v2]+0.5)
                    v = g.add_vertex(1,-2, rs[v2]+0.5)
                    phase = 0
                    g.add_edges([(n,v),(v1,n),(v2,n)],2)
                g.set_phase(v, phase + Fraction(3,4))

                for k in range(j+1,4):
                    v3 = group[k]
                    f = frozenset({v1,v2,v3})
                    if f in gadgets:
                        n,v = gadgets[f]
                        phase = phases[v]
                        if phases[n]:
                            phase = -phase
                            g.set_phase(n,0)
                    else:
                        n = g.add_vertex(1,-1, rs[v3]+0.5)
                        v = g.add_vertex(1,-2, rs[v3]+0.5)
                        phase = 0
                        g.add_edges([(n,v),(v1,n),(v2,n),(v3,n)],2)
                    g.set_phase(v, phase + Fraction(1,4))
        f = frozenset(group)
        if f in gadgets:
            n,v = gadgets[f]
            phase = phases[v]
            if phases[n]:
                phase = -phase
                g.set_phase(n,0)
        else:
            n = g.add_vertex(1,-1, rs[group[0]]+0.5)
            v = g.add_vertex(1,-2, rs[group[0]]+0.5)
            phase = 0
            g.add_edges([(n,v)]+[(n,w) for w in group],2)
        g.set_phase(v, phase + Fraction(7,4))