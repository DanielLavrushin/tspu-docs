# Chapter map, revision 2

Working input for the `/revise-chapter` sessions, not documentation. Built on 2026-10-28 from transcript/transcript.md (with the word timings in transcript/source/), the slides in transcript/slides/ and the memory notes (timestamp map, follow-ups).

How to read it:

- **Transcript.** Ranges are video times, H:MM:SS. "lines" are the transcript.md paragraphs that cover the range; a paragraph can start a little before the range. "Q&A" marks audience questions. "Also here" lists stretches whose home is another chapter but which this chapter summarises or links to.
- **Slides.** Number, first shown, title. ★ marks an image candidate (diagram, topology, hardware photo). "In chapter at file:line" means an image of that slide is already embedded. "Flip" means it was on screen for 1–2 seconds.
- **Follow-ups.** The open items from memory (tspu-docs-followups), checked against the slides and the transcript:
  - `[slide NNN]`, `[t H:MM:SS]`: supported; apply.
  - `[contradicted]`: the slides or transcript say otherwise; the evidence decides, not the item.
  - `[vendor-only]`: rests only on the documents in tspu-equipment/, so it is not a fact; don't apply.
  - `[editorial]`: about the chapters' own consistency; needs no source.
  - "(found in the check)" marks mismatches found next to a queued item.
- **Vendor-attributed lines.** Statements an earlier pass took from tspu-equipment/ («по документации производителя», «в новых версиях ПО» and similar), by line number as of 2026-10-28. Keep a fact only where the slides or transcript support it, drop the attribution, and remove and list the rest. validate.py reports them as `vendor` warnings.
- **Leads.** Discrepancies found while building this map that are not in the follow-up queue yet. "(seen)" means the slide was checked at full size for this map. Re-read the cited slide before changing a chapter.
- **Existing alt="image" images.** Each chapter session writes real alt texts for the images in its chapter, and a caption where one is missing. The validator warns until then and `--strict` fails on any left. Only replacing such an image is a proposal.
- **Changes from other sessions.** A fix that another chapter's session makes in this chapter is recorded at the end of the chapter's section.

At the end: coverage gaps, organisational stretches, boundary corrections against the memory map, and recurring recognition errors.

## Proposed new sections (awaiting approval)

A chapter session adds a new numbered section, removes one or renumbers sections only after the user approves it. Until then the material goes into the nearest existing section or waits, and the report says so.

| Proposal | Material and source | Status |
|---|---|---|
| 4.8 «Проектирование эшелона» | Q&A 1:31:47–1:35:02: jumper capacity, one operator LAG per balancer and the crossed scheme (hedged), design inputs, the «EHW or not» field in the balancer design template; sizing echelon filters with the type-A figures (1:32:21–1:33:25) | proposed, awaiting approval |
| 8.10 «NTP и TACACS на балансировщике» | 4:40:54–4:41:46 and slide 117: newer firmware adds the `ntp` and `tacacs` branches. No parameters are shown, so a paragraph in 8.1 may be enough | proposed, awaiting approval |
| A number for «## Общий порядок настройки балансировщика» (balancer-config.md:460), or folding it into the chapter's introduction | Editorial; the validator warns about the unnumbered `##`. If it gets a number, it and 8.10 need an order | proposed, awaiting approval |
| 9.8 «Bypass watchdog (GL Sun)» | 5:18:30–5:19:30 and slide 130: `show ecofilter-balancer bypass-watchdog-groups`, `state connected` / `disconnected`; now an unnumbered sub-heading in 9.7 | proposed, awaiting approval |
| 23.9 «Обращение в техподдержку» | 3:34:09–3:35:28 (the S/N from `show version` in every request) and 3:44:31–3:48:11 (escalate when tables pass 20 %, mbufs keep shrinking or CPU reaches 80–90 %). The agenda item on slide 001 was never presented | proposed, awaiting approval |
| Remove 16.6 «IPv6 в пуле», move its material to 15.4, renumber 16.7 → 16.6 | 3:09:59–3:11:00 and slide 070: `/ipv6` is its own section; the pool listing on slide 069 has no IPv6 block | proposed, awaiting approval |

Not new sections, so no approval needed: 14.10 already exists and gets the unused `protocol_log` block; additions to 4.3.1 and 22.9 (FlowSpec), 7.5 (connection settings), 8.1 (command tables and tree), 11.4 (log ports, IPMI), 15.2 (`alg`, `udp_inbound_refresh`), 17.1 (`shortlist`), 18.12 (log format), 19.3 (`copy hwinfo`), 20.4 (log values) and 21.4 (components); headings corrected to the slides' command names. The queued 22.4 dedupe keeps the numbering if 22.4 becomes a short overview with links; merging it away would renumber 22.5–22.10 and needs approval. Chapters 24 and 25 are already planned.

## Part I. Обзор системы

### 1. Введение и общая архитектура АСБИ · docs/overview.md

Transcript

- 0:00:51–0:08:18 (lines 13–35) АСБИ and the sovereign-internet law; participants (ФГУП ГРЧЦ, АО «ДЦОА», RDP.ru with the balancer, the filter and part of the management system); ТСПУ at the operators; ЦСУ on two independent sites; the subsystems; LAN/WAN; one bypass per operator link (10–100G, some 1G); balancers (32 ports, 1U, 3.2 Tbit/s); filters (count follows traffic, 10GbE to the balancers); the management part. 0:03:10–0:03:32 is a drawing check.
- 0:08:18–0:09:38 (lines 35–39) the simplest variant. Its home is 2.3; chapter 1 only refers to it.
- Q&A 1:14:50–1:16:06 (lines 271–277) the federal software differs from the Ural pilot; EcoHighway is the version tested in the Surgut test zone; filter software keeps gaining functions. Fits the pilot/federal remarks in 1.2.

Slides

- 001 0:00:00 agenda (the lecture plan, not content); 002 0:00:50 section title.
- 003 0:00:53 «Структура АСБИ» ★, in chapter at overview.md:18.
- 004 0:02:17 «Архитектура ТСПУ» ★, in chapter at overview.md:60. 005 0:02:40, 006 0:03:15, 007 0:06:18 and 008 0:07:39 show the same diagram under an overlay (dark box or popup); 004 is the clean one.
- 009 0:08:20 «Простейший вариант ТСПУ» ★, in chapter at overview.md:134. It moves to 2.3 with the material.

Follow-ups

- [editorial] The simplest-variant block (overview.md:126–138) and the closing paragraph on the typical configuration (:140) duplicate traffic-flow.md 2.3 (:90–117) and the start of 2.4 (:119–121). Keep the material in chapter 2 and cut chapter 1 down to references.
- [editorial] Write real alt texts for the three alt="image" images (overview.md:18, 60, 134).

Vendor-attributed lines: none.

Leads

- overview.md:16 expands ЦСУО as «центральная система управления»; slide 003 has «Централизованная система управления оборудованием».

Changes from other sessions: none yet.

### 2. Прохождение трафика через ТСПУ · docs/traffic-flow.md

Transcript

- 0:03:32–0:04:24 (lines 21–23) LAN towards the subscribers and WAN towards the internet, through the whole ТСПУ (2.2).
- 0:08:18–0:09:38 (lines 35–39) the simplest variant: one or two links, no balancer, one filter, the mandatory management part (VPN gateway, СПФС, СПХД); only 1/10GbE, because the filters have no 100G (2.3, home).
- 0:09:38–0:13:46 (lines 41–53) the typical scheme in four stages; the operator junction, local and remote addresses; extra encapsulation (none, VLAN, QinQ, MPLS, MPLS+VLAN, PPP inside MPLS) (2.1, 2.4).
- Q&A 0:33:19–0:35:01 (lines 125–131) even ports LAN and odd ports WAN, on the filters and the balancers; 100G ports by number (2.2; home 6.3.1).
- Q&A 0:36:37–0:38:28 (lines 137–143) a single session cannot be spread: a 200G session lands on one port and one core (2.4, stage 3).
- Also here, summarised in 2.4: the bypass 0:13:49–0:20:22 (lines 55–75) (home 5), the balancer 0:20:40–0:29:40 (lines 77–107) (home 6), the filter path 0:42:36–0:44:37 (lines 157–165) (home 10).

Slides

- 009 0:08:20 «Простейший вариант ТСПУ» ★, now in chapter 1 at overview.md:134.
- 010 0:09:37 «Прохождение трафика через ТСПУ» ★, in chapter at traffic-flow.md:9.
- 011 0:10:14 «Путь пакета 1» ★, in chapter at traffic-flow.md:35.
- 012 0:13:47 «Путь пакета 2» ★, in chapter at traffic-flow.md:156; 013 0:15:22 is the same under an overlay.
- 014 0:20:43 «Путь пакета 3» ★, in chapter at traffic-flow.md:177.
- 015 0:42:35 «Путь пакета 4» ★, in chapter at traffic-flow.md:223.

Follow-ups

- [editorial] Duplication with chapter 1, see there.
- [editorial] Write real alt texts for the five alt="image" images (traffic-flow.md:9, 35, 156, 177, 223).
- QUIC remark: «распознавание QUIC отдельным списком» [slide 075 `quic_list ( )`; t 3:28:15]. «Для QUIC (UDP/443) TCP Reset неприменим» [vendor-only: the lecture never says how QUIC is blocked].

Vendor-attributed lines: 231 («307 Temporary Redirect»).

Leads

- Slide 009 also says «Один фильтр (либо несколько независимых)»; check that 2.3 says so.

Changes from other sessions: none yet.

### 3. Места установки ТСПУ в сети оператора · docs/placement.md

Transcript

- 0:48:43–0:54:03 (lines 183–201) install point 1 before BRAS/BPE/BNG/GGSN/PGW (PPPoE, extra encapsulation); point 2 after BRAS and before CGNAT (grey addresses, the most convenient); point 3 after CGNAT (white addresses only, troubleshooting needs the operator's NAT data); BRAS and CGNAT in one box remove point 2; on-a-stick, where traffic crosses ТСПУ twice (cases 1+2, 2+3, 1+3).
- Q&A 0:54:03–0:57:31 (lines 201–213) on-a-stick capacity. Best when the operator separates the directions by VLAN and only one section's VLANs go to the filters (Ural example: CGNAT on a stick, only the pre-CGNAT VLANs); otherwise double sessions, confusing troubleshooting and double load. Excluding the listed VLANs instead works too.

Slides

- 016 0:44:37 «ТСПУ в сети оператора» ★, in chapter at placement.md:11. It flashes at 0:44:37; the heartbeat Q&A runs over 015 until 0:48:37, and 016 is back from 0:48:39.
- 017 0:48:39 flip; 018 0:52:40 «ТСПУ в сети оператора» (on-a-stick) ★, in chapter at placement.md:81; 019 0:57:37 flip.

Follow-ups

- [editorial] Write real alt texts for the two alt="image" images (placement.md:11, 81).

Vendor-attributed lines: 28 (encapsulations the balancer and filter parse), 36 (L2TP not described), 140 (rule conditions by subnet, tag count, frame type).

Changes from other sessions: none yet.

### 4. Эшелонированная система (ТСПУ тип Б) · docs/echelon.md

Transcript

- 1:01:55–1:10:33 (lines 231–257) purpose: traffic that bypasses type A (type A = first echelon = plain «ТСПУ»); operator layers: access/distribution with single-homed operators, core/peering with multi-homed ones whose sessions don't assemble on type A; EcoHighway gets lists from ЦСУ by BGP and itself blocks the IP part of the registry and the protocol IP lists; echelon filters only filter registry URLs, on-a-stick, LAN/WAN told apart by a VLAN tag; transparent pass of traffic that type A already handled; the slide-024 comparison.
- Also here: 1:14:01–1:14:50 (lines 269–271) the same lists go to EcoHighway by BGP (home 22).
- Q&A 1:14:50–1:16:06 (lines 271–277) federal vs pilot software; EcoHighway as tested in Surgut.
- 1:16:06–1:25:11 (lines 277–307) two pipelines in the chip, set up identically on EcoFilter-Balancer and differently on EcoHighway (twice the tables, TCAM); ports bound to pipelines at the factory; the jumper; LAN ports on one pipeline and WAN on the other (the even/odd rule is not kept); the BGP tables; three outcomes: drop, to the filters (filter-group), to the other pipeline.
- Q&A 1:25:25–1:37:09 (lines 307–351) EcoHighway keeps no logs, real time only (4.6); an operator says EcoHighway filters its BGP session: look up the IP and port 179 in the ЦСУ lists, check filter sessions, use software bypass (4.6; 23); a packet reaches the filters once and leaves through the pair port (p4-1 → p9-1); the jumper must carry all the traffic; echelon filter firmware is slightly faster (115 vs 100 Gbit/s), size with the type-A figures; one operator LAG per balancer, the crossed scheme probably impossible (hedged); no manual rules on EcoHighway; the balancer came first, the echelon later, to cut the number of ТСПУ.
- Also here: 4:28:23–4:29:03 (lines 953–955) same hardware, different software (4.5); 5:13:44–5:14:40 (lines 1109–1113) the per-group software bypass was ported from EcoHighway (4.5); 5:20:48–5:23:51 (lines 1135–1147) the Surgut echelon trial with all filters in software bypass.

Slides

- 021 1:01:25 section title (device photo).
- 022 1:01:53 «Эшелонированная система» ★, in chapter at echelon.md:13 (cropped, no caption).
- 023 1:05:05 «ТСПУ тип Б» ★ (type-B site topology), not used yet.
- 024 1:09:23 «Балансировщики для ТСПУ тип А и Б» (text).
- 025 1:10:33 «Формирование и загрузка списков фильтрации» ★ (home 22).
- 026 1:14:51 «EcoFilter-Balancer vs EcoHighway» ★.
- 027 1:19:44 «Путь пакета через EcoHighway» ★. Its WAN labels have a misprint: P9-2 twice, no P9-1.

Follow-ups

- [editorial] 4.7 already matches 3.4.3; its substance is at [t 1:08:57].
- [editorial] The image at echelon.md:13 (slide 022) needs a real alt text and a caption.
- The diagram at echelon.md:142 uses P41/P42/P91/P92; use `p4-1`-style names [slide 027: LAN p4-1…p4-4, WAN P9-x; t 1:31:27, where the speaker says the misprinted label should be p9-1, «самый правый»]. «P41» is a recognition artefact (1:20:48).
- One operator LAG per balancer, and the crossed scheme may not work because the echelon filters are on-a-stick: belongs in 4.3.3 [t 1:33:25–1:35:02, hedged: «скорее всего», «ответа пока однозначного нет»; slide 024 confirms on-a-stick]. 6.3.3 already covers the type-A side [editorial].

Vendor-attributed lines: none.

Leads

- «BGP FlowSpec» (slides 024, 025: lists «по протоколу BGP с использованием спецификации FlowSpec») is in no chapter.
- Slide 023: the type-B site has a bypass, EcoHighway, filters, a VPN gateway and СПХД, with BGP from ЦСУО over the management network.
- Slide 027 tables: IPv4+port, IPv4, IPv6+port, IPv6, IPv4/IPv6+mask+port, port-redirect; group names filter-group and ecofilter N. 4.3.1 folds the mask into IPv4+port.
- The design and scaling answers (1:31:47–1:35:02: jumper capacity, the LAG rule, design inputs, the «EHW or not» field in the balancer design template) have no section. Proposed as 4.8 «Проектирование эшелона», awaiting approval (see the top), plus items for 24.

Changes from other sessions: none yet.

## Part II. Байпас и балансировщик

### 5. Байпас (Bypass) · docs/bypass.md

Transcript

- 0:13:49–0:20:22 (lines 55–75) Silicom (federal) and simpler bypasses (Ural pilot); NET0/NET1 to the operator, MON0/MON1 to the balancer; Inline, TAP, Active Bypass, switching without flaps; Passive Bypass on power loss (optical, a link flap); GL Sun: passive only; heartbeats MON0→MON1 through the balancer, automatic switch to TAP or Active Bypass.
- Q&A 0:44:40–0:48:37 (lines 165–181) Silicom heartbeats don't reach the filter, the balancer turns them back; two stages of checks (bypass→balancer heartbeats, balancer→filter keep-alives); keep-alives are small non-IP packets turned back at the first check; without a balancer, the Silicom heartbeat (IPX by default; the RDP-supplied format is being set on all bypasses) passes the filter transparently.
- 3:11:00–3:12:02 (lines 677–679) the filter's `bypass` section: GLSUN heartbeats when there is no balancer, Ural pilot only (16.7).
- 4:33:46–4:34:17 (lines 971–971) the balancer and GL Sun (Ural only); with Silicom it passes the heartbeats between its ports.
- 4:55:09–4:55:54 (lines 1045–1047) Ural: active-pairs equalled all pairs, so one failed interface took the group down and the balancer switched the bypass.
- 5:03:39–5:05:50 (lines 1077–1081) the balancer's heartbeat settings for GL Sun (8.8); Silicom sends its own.
- 5:18:30–5:19:30 (lines 1127–1131) `show ecofilter-balancer bypass-watchdog-groups` (9.7).
- Q&A 5:20:48–5:23:51 (lines 1135–1147) Ural: a filter problem sends the whole site to bypass (link flaps, planned works to come back); the new logic bypasses per group without flaps.

Slides

- 012 0:13:47 «Путь пакета 2» ★ (bypass modes), in chapter 2 at traffic-flow.md:156; 013 0:15:22 is the same under an overlay.
- 071 3:11:00 «Настройка bypass»; 124 5:03:38 «Настройка отправки хартбитов и MNG интерфейса»; 130 5:14:39 watchdog status.

Follow-ups

- The GL Sun heartbeat transport is TCP [slide 124 `tcp-port 4001`; slide 130; t 5:19:01 «по протоколу TCP»]. The vendor's `udp-port` and `bypass-unit profile` [contradicted: slides 124 and 130 show one `bypass-watchdog-groups` block].
- (found in the check) The watchdog's normal state is `connected`, not `active` (bypass.md:161) [slide 130; t 5:19:12 `disconnected`]. «Active» is the state of the balance group.
- 5.3.1: the balancer reaches the bypass over the management network [slide 124 puts the bypass in the same /24 as `mng-if`; an inference, not stated].
- Filter-side heartbeats without a balancer go over UDP from MNG [vendor-only: slide 071 shows `bypass_ip`, `bypass_tos`, `bypass_interval`, `te1_te2 01` …, but no protocol or interface].

Vendor-attributed lines: 200 (Silicom heartbeat every 5 ms, «по документации Silicom»).

Leads

- 4:33:53 «…для пилотного проекта на Урале, для будущего федерального проекта» most likely means «…а не для будущего федерального» (compare 5:18:32 and slide 124).

Changes from other sessions: none yet.

### 6. Балансировщик: принцип работы · docs/balancer.md

Transcript

- 0:05:17–0:06:10 (lines 27–29) a programmable switch: 32 ports, 1U, 3.2 Tbit/s at wire speed above 160 bytes (6.2).
- 0:20:40–0:29:40 (lines 77–107) two port groups and LAN/WAN pairs, no default configuration; links (p4-2 + p4-1), traffic never moves between operator links; flow rules (to the filters or bypass; BGP TCP 179, multicast and routing protocols sent back); the balance group; the hash on src IP, dst IP, protocol plus the filter cores; the 4-byte header; the symmetric hash.
- Q&A 0:30:07–0:42:27 (lines 109–157) failover by keep-alives and per-group software bypass (the Ural pilot bypassed the whole site; the new software rebalances or bypasses one group); the LAN/WAN port convention (even/odd, 100G by number); finding a session's filter (no logs on the balancer; walk the filters, a script) (23.2); spreading 200G; MPLS: labels never stripped, matching on VLAN tags, non-IP passed through; HTTP 302 and TCP Reset inside one-way MPLS: the filter waits for the server's reply in the same session (6.8, 10.1.5).
- Q&A 0:44:40–0:48:37 (lines 165–181) keep-alives vs heartbeats (6.6.1; see 5).
- 4:30:17–4:34:17 (lines 957–971) slides 112–113: software bypass, wire speed, the main functions (interfaces, filters and cores, the pair-port rule, determinism, complex encapsulation, keep-alives, N+1 not used, offloading such as multicast, GL Sun).
- 4:45:05–4:46:11 (lines 1007–1013) `nat-unit-queues` = filter cores − 1 (6.5.2; home 8.5).
- 4:53:30–4:58:14 (lines 1039–1055) the liveness profile and active-pairs; the Ural behaviour; `rebalance` vs software bypass of a pair (6.6).
- 4:58:14–5:03:39 (lines 1055–1075) flow rules: actions, priority, apply-to-links, match conditions (6.4; home 8.7).
- 5:11:49–5:14:40 (lines 1103–1113) keep-alive statistics, time-on-path; the manual group bypass (6.6; home 9.6–9.7).
- Q&A 5:16:57–5:18:30 (lines 1123–1127) `initial-delay` is the wait after boot or after the filter-side interfaces come up.
- Q&A 5:20:48–5:26:26 (lines 1135–1157) automatic return from group bypass; filter table load can cost keep-alives; group flapping without link flaps; an SNMP trap only for fatal syslog messages.

Slides

- 014 0:20:43 «Путь пакета 3» ★, in chapter 2 at traffic-flow.md:177.
- 112 4:30:13 «Балансировщик» ★ (cable and transceiver photos; home 7.3); 113 4:31:15 «Основные функции».
- 121–123 (balance group, flow rules, match conditions; home 8), 129 (keep-alive statistics; home 9).

Follow-ups (from the chapter-8 checks and the 6.4 note)

- Priority: the lower number is checked first [slide 122 (seen): a rule at 100, the catch-all bypass at 65535; t 5:01:20 «с самым низким приоритетом»]. This settles «направление шкалы … противоречиво» at balancer.md:107.
- Match-condition names (balancer.md:134, «по документации производителя») [slide 123 shows them in the lecture's firmware: ip-proto, ipv4-src/dst, ipv6-src/dst, l4-port-src/dst, mac-src/dst, mpls-depth, packet-type, vlan-depth, vlan0-tag, vlan1-tag, vlan2-tag]. SCTP, DCCP, UDP-Lite and the LLC fields [vendor-only].
- 6.3.3: identical balance groups on every balancer and `show ecofilter-balancer balancing-config-hash` (balancer.md:97) [vendor-only].
- The old vs new configuration model (balancer.md:101) [the slides show only the old names; ecofilter-unit, pair, cores, to-ecofilter, drop, balancing-method, external-acl and bypass-unit are vendor-only; t 4:40:54: the slides' tree is from newer firmware than the Ural one].
- `initial-delay` (balancer.md:228) [t 5:17:16 and slide 121 «Начальная задержка»: a pause before the keep-alives start]; the «maximum allowed delay» reading [vendor-only].
- The manual group bypass (balancer.md:248) [t 5:13:44: such a command exists, with bypass and primary modes, name not remembered]; `call ecofilter-balancer set-bypass-ecofilter-unit …` [vendor-only].
- The factory firmware (balancer.md:23) [contradicted in part: t 4:46:11 «с завода … нет ни прошивки, ничего»; slide 126 does show a `Factory` image slot].

Vendor-attributed lines: 19, 97, 101, 107, 109, 130, 134, 158, 170, 228, 244, 248, 260, 266, 283.

Changes from other sessions: none yet.

### 7. Балансировщик: аппаратная платформа · docs/balancer-platform.md

Transcript

- 4:28:23–4:40:28 (lines 953–991) the same hardware as EcoHighway; the 1U 32-port and 2U («64, точнее 65») models, only 1U in the project; 10G and 100G typical; two hot-swap PSUs; the front panel (console, management, 32 QSFP, an unused diagnostic connector); software bypass, wire speed, breakout hydras (optical or DAC), management at 1 Gbit/s only; the slide-113 functions (home 6); the internal scheme: Ethernet switch, UART MUX, microserver (Linux, CLI) over PCIe to Barefoot Tofino, the pipelines inside Tofino, the BMC (health, PSUs, sensors; the spring incident where the BMC misread a sensor and powered off the microserver), the USB hub; connection: admin/admin over SSH, the console speed depends on whether you land on the BMC or the microserver.
- Also here: 0:05:17–0:06:10 (lines 27–29) 32 ports, 1U, 3.2 Tbit/s; 1:16:06–1:20:06 (lines 277–291) pipelines and the factory port binding (home 4.4); 2:57:48–2:58:26 (lines 627–629) the balancers run MTU around 9000.

Slides

- 110 4:28:17 section title (balancer photo).
- 111 4:28:30 «Балансировщик» ★ (ELB-0133 and ELB-0165 photos and specs).
- 112 4:30:13 «Балансировщик» ★ (breakout cable, transceiver and DAC photos).
- 113 4:31:15 «Основные функции».
- 114 4:34:15 «Внутренняя схема» ★ (block diagram).
- 115 4:39:26 «Подключение.» ★ (front panel photo).

Follow-ups

- 10/25/40/50/100GE [slide 111]; the project uses 10G and 100G [t 4:29:34].
- (found in the check) README 7.2 «10G / 25G / 100G» and the 8.3 speed list «10G, 25G или 100G» [contradicted in part: slide 119 says «10G, 40G, 100G»; 25G per lane is in speech, 4:47:53, and slide 111 lists it as a capability].
- Lanes 1–4 [slides 119, 127].
- ELB-0133 (1U) and ELB-0165 (2U) [slide 111; the spec blocks are headed «Bypass ELB-0133/0165», sic].
- «двухюнитовый (65 портов)» in README 7.1, the 7.1 table and 6.2 («2065 … 65 × QSFP28») [contradicted in part: slide 111 says «ELB-0165 – 64 порта QSFP28/QSFP+» and the photo shows ports 1–64 plus one unnumbered cage; t 4:29:09 «64 порта, точнее 65»].
- The EcoSwitch 1020/1032/2065 line-up [vendor-only; only the prompt `ecoswitch@admin>` appears, slides 127–129].
- 2.0/3.2/6.4 Tbit/s [3.2 for the 1U only: t 4:30:36 and slide 114 «32 x 100G»; the rest vendor-only].
- MTU 9000 [slides 117, 119, as the value in use]; that 9000 is the default, the range 64–10240, `fec` and `force-up` [vendor-only].
- Factory management IP 192.168.255.1/24 [vendor-only].
- Barefoot Tofino [slide 114 «Barefoot Toffino»; t 4:35:51]. That Intel stopped Tofino development is not in the lecture: an outside fact (in January 2023 Intel announced it was ending investment in its network-switch line). State it neutrally as current knowledge.

Vendor-attributed lines: none.

Leads

- Slide 111: dimensions, power draw (476 W / 1024 W), weight (10 / 14.3 kg), AC or DC PSUs. None of it is in the chapter.
- Slide 112: 4-channel QSFP+ PSM transceivers with MTP/MPO-12 → 8×LC cables for optical 10GE, and DAC cables to the filters; partly missing from 7.3.
- Slide 115: serial 9600 (38400) baud, 8N1, no flow control; SSH port 22; admin/admin. 7.5 has only the login and the speed guessing.
- 4:39:11 «…через этот USB, через мониторинг, а они напрямую с чипа Tofino» most likely means «…а не напрямую»: transceiver data reach the CLI over USB-UART (slide 114: QSFP28 → USB-UART → USB hub). The chapter's diagram lacks the USB hub, USB-UART, power controller and sensors.

Changes from other sessions: none yet.

### 8. Балансировщик: конфигурация · docs/balancer-config.md

Transcript

- 4:40:28–5:05:50 (lines 993–1081) the two modes and `edit`; the slides' tree is newer than the Ural firmware (NTP and TACACS added, ports moved to the root); `set`, a Juniper-like CLI; `apply` and `save` now separate; firmware in two steps, two images; the scheme again; `nat-unit-queues` = cores − 1; nothing configured from the factory; ports (label, number, lane, speed, mtu, description; lanes and hydras; p2 at 100G); links; balance groups and filter groups; the liveness profile (1000/100/5/5/8); Ural active-pairs; `rebalance`; flow rules: action, `balancing-as mag-hash`, `to-balance-group`, `bypass`, priority, empty match, `apply-to-links`, match conditions; GL Sun heartbeats (Ural only); the management interface; not needed with Silicom.
- Q&A 5:16:57–5:18:30 (lines 1123–1127) `initial-delay`.
- Q&A 5:19:42–5:20:48 (lines 1131–1135) the `tries` window, hedged («по-моему 20 минут», then «20 минут между попытками, три попытки в час»), and not configurable.

Slides

- 116 4:40:27 «Конфигурация» (command tables for both modes); 117 4:40:57 «Конфигурация» ★ (config tree); 118 4:43:02 «Прошивка»; 119 4:44:41 «Настройка физических портов» ★ (scheme and port block); 120 4:50:27 «Настройка линков»; 121 4:51:47 «Настройка линков и профиля проверки доступности…» (actually the balance group and the liveness profile); 122 4:58:31 «Настройка фильтров пакетов (1/2)» (seen); 123 5:02:38 «(2/2)» (match conditions); 124 5:03:38 heartbeats and MNG.

Follow-ups: the slides' syntax. Every form below differs from the chapter.

- Ports: `port { label p2-1 { number 2 lane 1 speed 10G mtu 9000 description … } }`, or `set port label p16-1 number 16 lane 1 speed 10G mtu 9000` [slides 117, 119; contradicted: `set ports p2-1 …`]. p2 has no lane at 100G [t 4:49:44].
- `nat-unit-queues 21` is a global line above `port {` [slide 119], not a balance-group setting [contradicted in part: the summary's step 5 and 8.5.2]. The slide's own note says 23 for a 24-core Xeon Gold 6212U.
- Links: `links isp_link_1 { lan p1-2 wan p1-1 description … }` [slide 120; contradicted: `set links … lan-port … wan-port`].
- Balance groups: `balance-groups group_filter { liveness-profile live_loop_or_not rebalance enable filter-group filter1_1 { lan p4-2 wan p4-1 } }` [slide 121; contradicted: `set balance-group … filter-group … lan-port … wan-port`].
- Liveness: `liveness-profiles live_loop_or_not { initial-delay 1000 interval 100 probes-down-count 5 probes-up-count 5 active-pairs 8 }` [slide 121; contradicted in part: `set liveness profile …`; the five names match]. The meaning of `initial-delay` [t 5:17:16]; the vendor reading at balancer-config.md:297 [vendor-only].
- Filters: `filters bypass_or_not { flows traffic_to_filter1 { priority 100 match { vlan0-tag 1 } action { balancing-as mag-hash to-balance-group group_filter } } flows bypass_all_others { priority 65535 action { bypass } } apply-to-links { isp_link_1 … } }` [slide 122]. `to-balance-group` sits inside `action` [contradicted: 8.7.2]. Filters live under `ecofilter-balancer` [slide 128 path].
- `match vlan 0 id 1` → `vlan0-tag 1` [slides 122, 123; contradicted; also in 23.4]. 8.7.1 lacks ip-proto, IPv6 and packet-type [slide 123].
- Priority: the lower number first [slide 122, t 5:01:20; contradicted: the 8.7.3 table runs 100 → 1, and 8.7.2 has `default-bypass … priority 1`].
- 8.7.3 «типовая структура» [slide 122 has that shape, but nobody calls it typical; t 5:03:26: a match can exclude or select]. Typical type-A rule sets are a few exclusions [t 1:05:31, 0:25:25]; slide 128 shows a live device whose one rule sends everything (empty match, priority 65535) to the filters.
- GL Sun heartbeats: `bypass-watchdog-groups live_link_bypass_or_not { ipv4 … tcp-port 4001 watchdog-delay 30000 (us) balance-group group_filter links { 01 02 … 32 } autoreturn enable type-of-service 184 }` [slide 124]. `bypass-unit profile`/`link-id` and `udp-port` [contradicted]. The defaults 10000 and 184, and «рекомендованное 30 мс» [vendor-only]. The speaker muddles the unit (5:04:12); the slide's 30000 us is 30 ms.
- Management: `mng-if { addresses default { ip … prefix 24 } routes default { destination 0.0.0.0 prefix 0 gateway … } }` [slides 124, 125; contradicted: `set management ip/mask/default-gateway`].
- Firmware: `call rdp-firmware download from-url … to-file …`, `call rdp-firmware install from-file …`, `list`, `remove`, `reset-tries`, `set-active`, `set-stable`, `set-factory`, `reboot` [slide 118; contradicted: `call rdp firmware download <URL> <файл>`, `call rdp install`, `delete`, and the README 8.2 heading].
- `tries`: 8.2.1 states «more than 3 failed boots in about 20 minutes» as fact [t 5:07:31 and 5:19:50–5:20:17, both hedged and different].
- Configuration mode: `edit` [t 4:40:36]; slide 116 lists both `configure` and `edit`.
- Names fixed earlier and confirmed: nat-unit-queues, liveness-profile(s), balancing-as mag-hash, apply-to-links, lanes 1–4, p2-1 [slides 119–122]. The GL Sun names: see above.
- [editorial] The unnumbered «## Общий порядок настройки балансировщика» at balancer-config.md:460: number it or fold it in, awaiting approval (see the top; the validator warns).

Vendor-attributed lines: 277 (`cores` in newer versions), 297 (`initial-delay` per the vendor guide).

Leads

- Slides 116–117: the command tables (operational: `configure`, `show`, `exit`, `help`, `call`, `edit`; configuration: `set`, `delete`, `show`, `exit`, `apply`, `end`, `up`, `edit`, `help`, `reset`, `save`, `delfile`, `loadfile`, `merge`, `op`, `dir`) and the root branches `ntp`, `ports`, `ecofilter-balancer`, `mng-if`, `tacacs`. 8.1 covers only the two modes, and NTP and TACACS on the balancer appear nowhere (8.10 is proposed at the top, awaiting approval).

Changes from other sessions: none yet.

### 9. Балансировщик: мониторинг и диагностика · docs/balancer-monitoring.md

Transcript

- 5:05:50–5:14:40 (lines 1083–1113) `show hardware-info`, `show mng-if`, `show rdp-firmware` (A/B, active, `tries`, stable), `call rdp-firmware reset-tries`, `show port …` (4 channels; no levels on DAC; frame counters), flow counters, the diagnostic bypass rule for one VLAN (23.4), `show ecofilter-balancer balance-groups` (keep-alives, time-on-path, 5 losses → group bypass), the manual group bypass (name not remembered, not in the current firmware).
- Q&A 5:14:40–5:18:30 (lines 1113–1127) time-of-receipt is an internal timestamp and the difference is time-on-path; the balancer knows nothing about DPI; `initial-delay`.
- 5:18:30–5:19:30 (lines 1127–1131) `show ecofilter-balancer bypass-watchdog-groups` (Ural only).
- Q&A 5:19:42–5:26:26 (lines 1131–1157) the `tries` window; automatic return from group bypass; whole-site bypass in the Ural pilot vs per group; table load and keep-alives; group flapping without link flaps; traps.
- Also here: 4:38:09–4:38:33 (lines 985–985) the spring incident (the BMC misread a sensor).

Slides

- 125 5:05:49, 126 5:06:36, 127 5:08:34, 128 5:10:05, 129 5:11:49 and 130 5:14:39, all «Отладка и мониторинг». 131 5:19:29 and 132 (flip) «Балансировщик. Вопросы?».

Follow-ups

- `show balance-group <имя>` [contradicted: slide 129 `show ecofilter-balancer balance-groups`]; `show liveness profile-status` [vendor-only]; `show ecofilter-balancer …` is the lecture's own syntax [slides 128–130].
- 9.6.2 «time-on-path резко возрастает» on loss [t 5:13:16]. The lecture's values are about 22–27 µs [slide 129]; 0 ns for a down pair and 128–150 µs [vendor-only].
- README 9.1 `show hardware info` with cpu/memory/fans/power/temperature [contradicted: slide 125 `show hardware-info all (cpu | fans | memory | platform-info | psu | sensors | storage)`].
- README 9.2 `show mng if` [contradicted: slide 125 `show mng-if`, whose output is the addresses and routes].
- README 9.3 `show rdp firmware version` and its sample output [contradicted: slide 126 `show rdp-firmware` → `boot-image { current A A { active true stable false version {… str 3.2.2.1.2647} tries 0 } B {…} Factory { active true stable true } }`].
- (found in the check) 9.4 `show port <порт> sfp` / `show port <порт> statistics`, power «в децибелах» [contradicted: slide 127 `show port tranceiver-eeprom port-number 2` (sic) with rx/tx power in mW, and `show port statistic port p2-1`; the speaker does say «в децибелах», 5:09:27].
- 9.5 `show filters <фильтр> flows <правило>` [contradicted in part: slide 128 `show ecofilter-balancer filters bypass_or_not flows traffic_to_filter`].
- 9.7 and 23.4 `call ecofilter-balancer set-bypass-ecofilter-unit …` [vendor-only; t 5:13:44].
- The watchdog state `connected` [slide 130]; see chapter 5.

Vendor-attributed lines: none.

Leads

- `bypass-watchdog-groups` is an unnumbered sub-heading under 9.7 (software bypass). Proposed as 9.8 «Bypass watchdog (GL Sun)», awaiting approval.
- 9.3 states the «3 failures in 20 minutes» rule as fact; keep the speaker's hedge.

Changes from other sessions: none yet.

## Part III. Фильтр

### 10. Фильтр: принцип работы · docs/filter.md

Transcript

- 0:42:36–0:44:37 (lines 157–165) the path through the filter: in through the LAN port; non-IP to the paired port; an ACL bound to a pool, otherwise transparent; DPI-list subnets, otherwise transparent; DPI: pass or drop.
- Q&A 0:40:26–0:42:27 (lines 149–157) redirect and TCP Reset inside one-way MPLS: the filter waits for the server's reply in the same session (10.1.5; 6.8).
- 2:51:23–2:52:50 (lines 609–611) the filter as an L2 wire; only management is visible to Linux, the rest is DPDK (10.2).
- Also here, summarised in 10.1–10.2 (homes 15–17): 2:54:01–3:03:30 (lines 615–649) nat_defaults; 3:03:30–3:12:02 (lines 649–679) ACL, pool and the bypass section; 3:12:02–3:34:09 (lines 679–755) DPI.
- Q&A 4:00:40–4:04:37 (lines 853–865) degradation acts only for protocols listed in a DPI list; the RKN section in the federal project; `no_ip` before `ip`.
- Also here: 4:10:08–4:16:40 (lines 885–909) recognition (10.1.4; home 22).

Slides

- 015 0:42:35 «Путь пакета 4» ★, in chapter 2 at traffic-flow.md:223 (re-shown 0:44:45; 017 is a flip). Configuration slides 065–077 (homes 15–17).

Follow-ups (found in the checks of chapters 15–17)

- 10.2: l2mtu maximum 9692 and the later default 9216 (filter.md:182) [contradicted in part: t 2:57:52 «максимально возможное по RFC – 9216», default «по-моему 1.52»].
- Long-idle TCP connections (filter.md:189) [vendor-only].

Vendor-attributed lines: 70, 72, 101, 111, 124, 126, 128, 155, 159, 160, 168, 180, 182, 189. Lines 126 and 128 cite «руководство EcoSGE 3.1.8»; 128 is the RKN `list_number` default, which slide 073 gives as 0.

Changes from other sessions: none yet.

### 11. Фильтр: аппаратная платформа · docs/filter-platform.md

Transcript

- 1:47:14–1:55:29 (lines 387–413) the slides are partly outdated; junior EcoFilter 2020/2040, senior 4080/4120/4160; «up to 160 Gbit/s» is NAT, not DPI; the 2019 hardware (Xeon E5-2695 v4 / E5-2699 v4, 128/256 GB, 32 GB SSD, log ports); the 2020 hardware (Xeon Gold 6212U, 24 cores, 192/384 GB, 4×10G SFP log ports, replaceable modules); odd ports WAN, even LAN; the standard blue box or black Lanner platforms; the rear panel and hot swap; history since 2013 (CG-NAT → URL filtering → BRAS → router → DPI); the EcoSGE platform and its licences; the project uses EcoFilter + EcoDPI.
- Q&A 4:22:29–4:27:00 (lines 929–947) log ports on the 2020 chassis: four SFP+ next to MNG and LOG/IPMI, te17–te20 in the configuration, labels may differ on Lanner boxes; the first batch is Lanner; the copper LOG/IPMI port carries IPMI only, logs stay on the log ports (separate subnets and switches).
- Also here: 0:06:10–0:07:44 (lines 29–33) the filter count follows traffic, 10GbE to the balancers; at 0:09:21, no 100G on the project's filters.

Slides

- 032 1:47:13 section title (filter photo).
- 033 1:47:23 «Фильтр» ★ (photos; size, power, weight).
- 034 1:48:57 «Фильтр» ★ (line-up photos).
- 035 1:49:36 «Фильтр 2019. Аппаратная часть.» ★ (labelled photo).
- 036 1:50:48 «Фильтр 2020. Аппаратная часть.» ★ (labelled photo; re-shown 4:22:54 for the log-port question).
- 037 1:52:36 «Фильтр 2019. Аппаратная часть.» ★ (rear photo).
- 038 1:53:10 «История» ★ (timeline); 106 is a flip of it.
- 039 1:54:29 «Платформа EcoSGE» ★ (licence diagram).

Follow-ups

- [editorial] The 11.1 heading «EcoFilter 2020/2040» vs the table rows «EcoFilter 20 / 40» (filter-platform.md:7, 13–14). The slides say 2020/2040 [slides 033, 034; t 1:47:47].
- Models 3060 and 5200, 100GE only on the 5200 [vendor-only; t 0:09:21: no 100G on the project's filters].
- «EcoFilter на платформе EcoSGE» [slides 039, 065; the CLI prompt `EcoSGE:`].
- Xeon Gold 6212U, not 6212 (filter-platform.md:63, 67, 73; balancer-config.md:273) [slides 036, 119]. The 2019 CPUs are E5-2695 v4 / E5-2699 v4, with DDR4-2666 ECC [slide 035].
- The 8.5.2 core table (18/22/24 → 17/21/23) [slide 119; the core counts from 035/036].
- (found in the check) 11.2 «все модели… вентиляторы, заменяемые на горячую» [contradicted in part: slide 034 gives hot-swap cooling only to the 4080/4120/4160].

Vendor-attributed lines: none. Lanner at filter-platform.md:82 comes from 1:52:22.

Leads

- Slide 033: dimensions, power (140/170 W; 285/400/400 W), weights (7.5 / 12 kg). Slide 034: 6 copper 1G ports on the 2020/2040. Slide 037: 4 fan modules, 2 × 500 W PSUs.
- 11.6 (filter-platform.md:138) says QoS where slide 039 has EcoQoE.
- The log ports te17–te20, the front labels SFP1–SFP4, and the rule that the IPMI port carries no logs (4:22:29–4:27:00) are missing.

Changes from other sessions: none yet.

### 12. Фильтр: сессии и трансляции · docs/filter-sessions.md

Transcript

- 1:55:29–2:08:19 (lines 413–459) classic NAT (local, global, remote; direction set by the first packet; last-packet and deletion times); no NAT in the project (local = global; IPv6 lines have no global part); the record format; the local IP always comes first, and Internet addresses on the local side mean a LAN/WAN mix-up (23.6); translation vs session, `show xlate` / `show sessions`; many sessions per translation; timeouts set separately (in the pool); examples with `lap`, `| count`, `| more`; filter keywords; the pipes include/exclude/count/more.
- Q&A 2:08:49–2:12:49 (lines 461–475) chained pipes (not in every command); no API: run `ssh admin@<IP> "<команда>"` from scripts; quote the command, the CLI pipe may fail over ssh, so use Linux tools; `| i 6881 | c`.
- Also here: Q&A 0:35:01–0:36:37 (lines 131–137) finding the filter that holds a session (no logs on the balancer; walk the filters, a script does about 15 in 10 s) (23.2).

Slides

- 040 1:55:28 «NAT» ★ (diagram); 041 1:58:51 «No NAT» ★ (diagram); 042 1:59:33 «Сессии»; 043 2:02:43 «Сессии и трансляции (1/2)»; 044 2:06:35 «(2/2)». Flips 103–105 at 4:22:49–51.

Follow-ups

- filter-sessions.md:19 defines Local as «серый, до NAT»; behind the operator's CGNAT it is the white NAT-pool address [t 0:51:18, 1:59:01; slide 042 defines it only as «локальный IP адрес абонента»].

Vendor-attributed lines: none.

Leads

- Slides 043/044: `show sessions`, `show xlate`, and the keywords `local`, `global`, `remote` (IP), `lap`, `gap`, `rap` (IP:port), `lport`, `gport`, `rport`. The chapter has `show session`, `show xl` (filter-sessions.md:37, 136, 143) and `la/ga/ra` (154–156), and so does README 12.8.
- Slide 044 pipe options also include `begin`, `drop`, `regexp`, `take`, and the short forms `i` and `c`.
- The `ssh … "<команда>"` technique applies to the whole CLI; chapter 13 may be its better home.

Changes from other sessions: none yet.

### 13. Фильтр: первоначальная настройка и CLI · docs/filter-cli.md

Transcript

- 2:12:49–2:22:39 (lines 477–509) console or SSH, admin/econat, port 22, 115200 8N1; the tree (`system`, `pools`, `acls`; branches such as bras and qoe_log are absent from project configs; the factory config has no pools or ACLs); `>` and `#`, `config`; navigation by branch name, `exit`/`..`, `root`/`/`; `apply` (syntax check, doesn't save) and `wr`; hotkeys; startup/effective/lastapply/factory, `clear config` loses SSH after apply, save/load/copy/erase; two users: the last apply wins, use `load effective`.
- 2:31:30–2:34:25 (lines 539–549) the «мышеловка» (an unclosed bracket); a bare `description` + Enter drops into the parameter; `… ls`.
- Also here: Q&A 2:09:13–2:12:03 (lines 463–473) running commands over ssh from scripts (now in 12.8).

Slides

- 045 2:08:24 «Первоначальная настройка» ★ (front photo with the console port); 046 2:13:28 «Конфигурация» ★ (tree diagram); 047 2:16:54 «Изменение конфигурации»; 048 2:18:58 «Управление конфигурациями»; 054 2:31:29 «"Мышеловка" CLI»; 055 2:33:05 «Ещё две особенности CLI». Flips 102 (4:22:47) and 107 (4:27:48).

Follow-ups

- The root branches are `system`, `pools`, `acls` [slide 046], and management is `mng_if` [slides 046, 053, 054] [contradicted: `access-lists` (filter-cli.md:40, 55) and `mng-if` (47, 67, 74, 75), also in README 13.4].
- The quick jump is `goto`, one word [slides 068, 069]; ordinary navigation is by branch name [slide 046, t 2:15:45]; `up` and `top` [slide 054].
- `edit` as a filter navigation command [vendor-only; configuration mode is `config`, t 2:15:16].

Vendor-attributed lines: none.

Leads

- 13.6 lacks `lastapply`, `dir` and `erase` [slide 048]. Slide 047 shows `write`. Unapplied edits are lost when the session drops (2:16:55–2:18:01).

Changes from other sessions: none yet.

### 14. Фильтр: конфигурация подсистем · docs/filter-subsystems.md

Transcript

- 2:28:22–2:31:30 (lines 527–539) the console port `/system/serial` (speed, inactivity timeout, `never` is bad); `mng_if` (IP, gateway, DNS, allowed IP; `+=` and `-=`).
- 2:34:25–2:48:40 (lines 549–599) the terminal (autologoff `never` piles up dead sessions to the limit of 20; prompt; line numbers); users (`create user … level … secret 0`, `no user`); TACACS (fallback to the local base); NTP (three servers, `show ntp`); SNMP (traps, read-only community, allowed IP); syslog (СПХД, two servers, `timeskew`, future time handling); `verbose` levels (default 1; user commands logged at FATAL; traps only for FATAL); `connection_log` through the LOG interface (no IP, DPDK), probably unused.
- 2:48:46–2:51:23 (lines 601–607) `debug_logger` to СПФС (protocols, 3 packets is enough, server, gateway, port, log interface); the `protocol_log` block is unused (14.10; 22.6).
- Also here: 5:25:22–5:26:26 (lines 1153–1157) an SNMP trap only for fatal messages.

Slides

- 052 2:27:41 COM port; 053 2:29:23 MNG; 056 2:34:24 terminal; 057 2:36:18 users (seen); 058 2:37:13 TACACS; 059 2:38:31 NTP; 060 2:39:32 SNMP; 061 2:40:25 syslog; 062 2:46:10 NAT-translation logging (/system/connection_log); 063 2:48:40 connection logging (4 s); 064 2:48:44 protocol logging. Flips 099 and 100 (4:22:43–44), 108 (4:27:49).

Follow-ups: none queued.

Vendor-attributed lines: none.

Leads

- 14.5: the parameter is `fallback on`, not `fb on` (filter-subsystems.md:100, 105) [slide 058].
- 14.4 and README «secret 0 / 15»: slide 057 (seen) creates users with `secret 0 "…"` and stores them as `secret 5 $5$…`; 15 is the privilege level. «secret 15» in speech (2:36:47) is a slip; the chapter has it at :78.
- 14.1: slide 052 offers never/2/5/10/15 min, and a change needs a reboot. 14.3: the names `autologoff_timeout`, `max_consoles` (2–100), `print_line_num`. 14.2: `name_servers +=(8.8.8.8)`, with parentheses. 14.8: `timeskew`, level 0, `show verboselvl`, `setlog` (slide 061).

Changes from other sessions: none yet.

### 15. Фильтр: настройка интерфейсов и общих параметров · docs/filter-interfaces.md

Transcript

- 2:51:23–3:03:30 (lines 609–649) interfaces (fixed LOG ports, LACP unused, enable/disable/description); `nat_defaults`: `vlan_mode` (default untagged, must be qinq), `alg` not needed, `sessions_per_translation` 4096, `udp_inbound_refresh` irrelevant, `forward_traffic on` (off only on a mirror), `l2mtu` (default «по-моему 1.52», set to 9216, the RFC maximum; balancers about 9000), three NAT-only parameters skipped, `lldp off` at the operators' request («по-моему МТС»), `permit_invalid_flow on` (sessions without a SYN after a return from bypass, and asymmetric traffic); the timeouts are a template copied into pools; `limiter` is NAT-only.
- 3:09:59–3:11:00 (lines 673–675) the `/ipv6` section: enable, timeouts, range (by default all addresses and all VLANs) (15.4).

Slides

- 065 2:51:23 «Настройка интерфейсов»; 066 2:54:00 «Настройка общих параметров CG-NAT (1/2)»; 067 3:02:15 «(2/2)»; 070 3:09:58 «Настройка IPv6». Flip 098 (4:22:42).

Follow-ups

- The names `nat_defaults`, `vlan_mode`, `l2mtu`, `sessions_per_translation`, `udp_inbound_refresh`, `forward_traffic`, `alg { ftp pptp rtsp sip alg_on_bnat }` [slide 066]; `timeouts_inactivity` [slides 067, 069, 070; the tree on 046 prints `timeout_inactivity`]; `limits_peruser { portlimit_icmp/tcp/udp }` [slide 067; spoken as «limiter»].
- 15.2.5 MTS is hedged [t 2:59:05 «по-моему»]; the chapter says «МТС потребовал».
- `inner_vlan` / `outer_vlan` and `pppoe_analyzer` [vendor-only].
- Additions to 15.2.6: the rebalancing case [t 4:56:21, in part]; long-idle TCP [vendor-only]; «global, not per pool» [slide 066 puts it under nat_defaults and the pool listing on 069 lacks it, but the nat_defaults timeouts are only a template, slide 067]; «needs apply» [only the general rule, t 2:16:59].
- (found in the check) l2mtu maximum 9692 and the later default 9216 (filter-interfaces.md:56) [contradicted in part: t 2:57:52 «максимально возможное по RFC – 9216»].

Vendor-attributed lines: 56.

Leads

- `alg`, `udp_inbound_refresh` and the three NAT-only parameters are not in the chapter. The vlan_mode default (untagged) is only in 10.1.1.
- 16.6 «IPv6 в пуле» belongs here (proposed, awaiting approval; see chapter 16).

Changes from other sessions: none yet.

### 16. Фильтр: ACL и пулы — запуск трафика на обработку · docs/filter-acl-pools.md

Transcript

- 3:03:30–3:09:59 (lines 649–673) a pool plus an ACL are needed, or traffic passes untouched; `create acl fake` → `aclfake`, `goto aclfake`; rules (numbering gaps, allow/permit/deny, ip/tcp/udp/icmp, host/net/any, VLAN 0–4095, one or a range, `no N`, `ls`); the pool: `create pool`, `acl <name>`, type `fake`, `enable`; priority; hairpin, connection_logging («по-моему включено»), timeouts and limits copied from nat_defaults.
- 3:11:00–3:12:02 (lines 677–679) the `bypass` section (GLSUN heartbeats, Ural pilot only) (16.7).

Slides

- 068 3:03:28 «Настройка ACL»; 069 3:07:26 «Настройка пула типа fake»; 071 3:11:00 «Настройка bypass» (its path label says «/ ipv6», a copy error). Flip 097 (4:22:41).

Follow-ups

- `create acl <name>` creates `acl<name>`, then `goto acl<name>` [slide 068; t 3:04:51]. The chapter doubles the prefix (`create acl aclfake` → `go to aclaclfake`) at filter-acl-pools.md:21–25, 71–72, 86–87, 114, 127–134 [contradicted]. `create pool fake` → `poolfake` [slide 069].
- The rule form: `10 permit tcp any any`, `15 allow ip host 10.10.10.10 any`, `5 deny ip net 192.168.1.0/24 any`; `allow` is stored as `permit`; `src`/`dst` are added automatically [slide 068].
- VLAN is a `~` suffix on the address: `0.0.0.0/0~101`, `~301-399`; by default `~0-4095` [slide 068]. VLAN 0–4094 [contradicted: 0–4095, slides 068 and 070; t 3:06:17]. `[port p]` [vendor-only].
- Binding: `acl aclfake` inside the pool [slide 069; t 3:07:43]; `use <acl> <pool>` [vendor-only].
- Default type `cgnat`, enabled by default, equal priorities [vendor-only]. `priority 100` appears in the new pool's listing [slide 069] but is not called a default. «The smallest priority wins» (16.4) is not in the sources either.
- `connection_logging on` in the example [slide 069]; the speaker hedges (3:09:10) and the chapter drops the hedge.
- 16.7: `system.bypass` with `bypass_ip`, `bypass_tos`, `bypass_interval 10` and `te1_te2 01` … [slide 071]; ms and 1–2000 [vendor-only]; UDP `<BP01_XX_BP>`, sent from MNG, the name «EcoBypass» [vendor-only].

Vendor-attributed lines: none.

Leads

- 16.6 «IPv6 в пуле»: nothing supports it. `/ipv6` is a separate section (slide 070) and the pool listing on 069 has no IPv6 block. Moving it to 15.4 (README included) is proposed at the top, awaiting approval.
- `randomize_ports` (slide 069) is not described.

Changes from other sessions: none yet.

### 17. Фильтр: настройка DPI · docs/filter-dpi.md

Transcript

- 3:12:02–3:34:09 (lines 679–755) pilot (RKN in dpilist 0) vs federal (a separate `rkn` section); `enable`, and disabling DPI as a diagnostic; `extra_analyze` obsolete; `send_rst off` (reconnect storms slowed phones); `functionality_mode`; dpilists 0–16; `shortlist`; `rkn` (source rkn/grfc, login, list_number, proxy, upload_dump_server); degradation `capacity` 0–100 (2–10 noticeable, about 5 gives delays of tens of seconds); list parameters (`whitelist_mode`, `log_matches`, `log_pictures`, `exceptions`, `behaviour` block/ignore/color/redirect, `redirect_url`, colouring, `download_url`, `update_schedule` and the `never` pitfall, `protocols`, per-list capacity unused, `quic_list`, `no_ip`, `no_ip_remote`, `ip`, `ipv6`, `no_ipv6`); the list format: HTTP matches a URL, HTTPS only the domain.
- Q&A 3:32:32–3:34:09 (lines 749–755) https lines block the whole domain.
- Q&A 4:00:40–4:10:08 (lines 853–885) degradation only for protocols listed in a DPI list; the RKN settings move from dpilist0 to a separate `rkn` section; `no_ip` first; «RKN list last downloaded 24 h ago» events (RKN published no delta; the filter polls every `update_schedule`, about 30 min); real download failures below about 10 Mbit/s; a temporary file during the download; `dpilist` and `list0.dpi`.
- Also here: Q&A 0:40:26–0:42:27 (lines 149–157) redirect and RST inside MPLS.

Slides

- 072 3:12:00 «Настройка модуля DPI» (re-shown 4:02:41); 073 3:17:44 «Настройка списка РКН»; 074 3:19:37 «Настройка деградации протоколов» (re-shown 4:00:53); 075 3:21:46 «Настройка списков фильтрации модуля DPI» (re-shown 4:01:48–4:04:25; 092 4:01:57 is the same with pen marks); 076 flip; 077 3:30:24 «Пример листа фильтрации» (re-shown 3:32:38). Flips 095 and 096 (4:22:39–40).

Follow-ups

- QUIC: `quic_list ( )` [slide 075, t 3:28:15]. «Recognition only», `quic_sni_match`, «closed by RST» [vendor-only].
- The names `whitelist_mode`, `log_matches`, `log_pictures`, `exceptions`, `behaviour`, `redirect_use_interval`, `redirect_interval`, `redirect_interval_url`, `redirect_url`, `color_direction`, `color_tos_byte`, `download_url` [slide 075].
- `update_schedule interval <X>` or `never`, in seconds, example 1800 [slide 075; t 3:27:11, 4:07:16]. The 17.4.6 table says minutes (filter-dpi.md:225) [contradicted]. «≥ 3600 recommended» [contradicted in part]; «never below 300» [vendor-only].
- `protocols` values are lowercase [slide 074, in part: telegram, whatsapp, viber, viber_voice, whatsapp_voice].
- `no_ip`, `no_ip_remote`, `ip`, `no_ipv6`, `ipv6` [slide 075]; `no_ip` is checked first [t 4:04:15].
- The branch is `dpilistN` [slides 046, 072, 075]; 17.4.1 shows `dpi list <N>` (filter-dpi.md:157) [contradicted].
- `functionality_mode normal_nat` / `double_mirrored_traffic` [slide 072]; `send_rst` and `extra_analyze` [slide 072], which the chapter writes as «send RST» and «extra analysis».
- 17.2.1 «ГРФЦ» = `grfc` [slide 073; t 3:17:59]; «ГРЧЦ» [vendor-only].
- The RKN list is stored as `list0.dpi` [t 4:09:38].
- `upload_dump_server` [slide 073]; FTP/TFTP [vendor-only] (HTTP/FTP/TFTP belongs to `download_url`).
- RKN `list_number` default «none» [contradicted: slide 073 `list_number 0`; t 3:18:46 «по умолчанию ноль»]; `list_number_soc` [vendor-only].
- 17.1.2: the RST storms slowed phones, not the filter [t 3:14:49–3:15:06]; remove the filter-load claim at filter-dpi.md:44, 46.
- 17.3: degradation acts only for protocols enabled in a DPI list [t 4:01:25, 4:02:15].
- README «17.4 (0–16)» [slide 046; t 3:16:32].

Vendor-attributed lines: 148 (`create dpilist N`), 195 («307 Temporary Redirect»).

Leads

- The `shortlist` section (3:17:07–3:17:41, logging of DPI-list hits) is in no chapter.

Changes from other sessions: none yet.

### 18. Фильтр: мониторинг и диагностика · docs/filter-monitoring.md

Transcript

- 3:34:09–4:00:22 (lines 755–849) `show version` (detail and hashes; the S/N = the management MAC, needed in every support request); `show ipif`; `show time`; `show uptime` (EcoNAT starts later; odd values after an NTP jump); `show power`, `show fan`, `show temperature` (40–50 °C normal, about 70 hot); `show interface brief` and traffic monitor; transceivers (`show sfp`; no DDM on copper and DAC; any vendor's module if the Intel chip supports it); `show resources` (tables below 20 %); free mbufs trend; DPI buffers below 100 %; CPU load is EcoNAT's share, 80–90 % still fine; control vs data plane (`show memstat`); free memory ≥ 5 % (some MTS builds compute it differently); `show cps`; `show statistics` (Optimal = 20 %); `show counters all` / `diff`, `clear counters`; `show logs` (two rotating files; external logging in the federal project); `show dpirecords`, `show dpistate`, `dpiload`, `dpirun`, `show dpimatch` (not in the Ural version); ping and traceroute from configuration mode. Inside: Q&A 3:44:31–3:46:09 (tables at 25–30 % → support; memory thresholds) and 3:54:11–3:55:03 (unrecognised packets); 3:43:45–3:44:31 is lunch-break talk.
- Q&A 4:04:37–4:10:08 (lines 867–885) dump-age events and the `show dpistate` fields; the temporary file; `dpilist`, `list0.dpi`.
- Q&A 4:16:40–4:17:25 (lines 909–911) ping and traceroute only check the management path.
- Q&A 5:23:51–5:26:26 (lines 1149–1157) table load can cost keep-alives; monitor the table load with a trigger above Optimal.

Slides

- 078 3:32:29 «Отладка и мониторинг работы фильтра (1/11)» through 088 4:00:01 «(11/11)»: 079 (2/11), 080 (3/11), 081 (4/11), 082 (5/11), 083 (6/11), 084 (7/11, seen), 085 (8/11), 086 (9/11, seen; re-shown 4:05:14), 087 (10/11). 089 4:00:21 «Фильтр. Вопросы?» (re-shown 4:16:44 and 4:27:57; 109 at 4:28:16 is a flip of it). Flips 090, 091, 093, 094.

Follow-ups

- `behavior` → `behaviour` at filter-monitoring.md:305 [slides 075, 077, 087].

Vendor-attributed lines: none. The Ural note at :309 comes from 3:59:22.

Leads

- The slides' command names differ from the chapter and the README:
  - `show counters diff` and `clear counters` (slide 084, seen; the chapter has `div` at :221, 228, 230);
  - `show dpirecords`, `show dpistate`, `dpiload`, `dpirun` (slide 086, seen; the chapter uses spaced forms);
  - `show dpimatch` (087; the chapter and 23.3 have `show dpi match`);
  - `show logs` (085; the chapter has `show syslog` at :244, 255);
  - `show ipif` (078; `show ip if` at :20, 22);
  - `show statistics` (083; `show statistic` at :207, 209);
  - `dpilist` and `list0.dpi` (the chapter has `dpi list` and `list_0.dpi` at :288);
  - the firmware string `3.1.4.0.40.bp` (078; `3.14.040 BP` at :15);
  - not named in the chapter: `show sfp teN` (081) and `show memstat` (082).
- Slide 085: the log record format `<date time> <subsystem> [<level>]: <message>` and the levels 0 FATAL … 3 INFO.

Changes from other sessions: none yet.

### 19. Фильтр: обновление прошивки · docs/filter-firmware.md

Transcript

- 2:22:39–2:28:22 (lines 511–527) the `firmware` commands; the FALLBACK partition, prim1/prim2 equal; `firmware status` (cur, boot); `firmware download` from a URL, `firmware install` into the inactive partition, one install per reboot; `firmware rollback` / `firmware revert`; reboot with confirmation from configuration mode, the CLI may not respond during the install; central updates from ЦСУ with a report. Q&A 2:27:41–2:28:22: reboot from ЦСУ «probably», mass reboots one by one.

Slides

- 049 2:22:38 «Работа с образами ПО» (re-shown 2:24:42); 050 2:24:20 (same, highlighted); 051 2:26:08 «Обновление ПО» (seen). Flip 101 (4:22:46).

Follow-ups: none queued.

Vendor-attributed lines: none.

Leads

- Slide 051 (seen): `firmware rollback` and `firmware revert`, then `reboot` with «Confirm (y/N)». The chapter and README 19.4 say `firmware reset` (filter-firmware.md:79, 86, 95, 97); 19.3 says `reload` (:76).
- The slides' versions are `3.1.4.0.31.bp` and `3.1.4.0.38.bp` (the chapter has «4031» at :30); the output label is `FALLBACK`.
- Slide 050: `copy hwinfo <адрес>/<файл>`, not spoken, in no chapter.
- 19.5 states as fact that reboots are done from ЦСУ; the speaker only supposed so (2:27:41).

Changes from other sessions: none yet.

## Part IV. Управление и блокировка

### 20. Сегмент управления ТСПУ · docs/management-segment.md

Transcript

- 0:57:39–1:01:25 (lines 215–229) the speaker warns that the log-subnet part of the slide is probably inaccurate and that the customer's team designs the segment; 10.<region>.<site>.0/24 (Moscow 10.77); allocation: .1–.128 bypasses, .131–.140 balancers, .141–.150 balancer BMC, .151–.190 filters, .191–.230 filter IPMI, .231–.235 СПФС management, .241–.245 СПФС IPMI, two СПХД (syslog) addresses, .254 the gateway on «Континент»; the log subnet is the same at every site; «Континент» builds a VPN to ЦСУ.
- Also here: 0:07:44–0:08:18 (lines 33–35) the management part in the overview; Q&A 4:25:15–4:27:00 (lines 941–947) the IPMI and log subnets are separate and on different switches.

Slides

- 020 0:57:38 «Управление ТСПУ» ★ (seen), in chapter at management-segment.md:11 (cropped, no caption, the slide-number badge still visible). 019 0:57:37 is a flip.

Follow-ups

- [editorial] The image at management-segment.md:11 (slide 020) needs a real alt text and a caption.

Vendor-attributed lines: none.

Leads (slide 020, seen)

- 20.2 (management-segment.md:42–58) gives .231–.235 to «SPFS (management + IPMI)» and .241–.245 to СПХД. The slide has .231–.235 СПФС mng, .241–.245 СПФС ipmi, and СПХД at .129 (mng) and .130 (ipmi).
- 20.4 lacks the slide's log values (172.31.255.0/24; filters .1–.20, СПФС .201–.210, «Континент» .254), and the speaker's caveat that this part of the slide may be wrong.

Changes from other sessions: none yet.

### 21. Центральная система управления (ЦСУ) · docs/central-management.md

Transcript

- 1:37:09–1:40:36 (lines 351–363) two independent data centres (main and reserve), entry through «Континент» gateways, an IP VPN from every site to both, users over an encrypted VPN; about 350 sites and 5000 devices; components: list forming, logging, monitoring, cartography.
- Q&A 1:41:12–1:43:31 (lines 365–373) DevOps run ЦСУ; ТСПУ software is loaded «вместе с ДП» (probably РДП); the СПФС servers are DevOps' job too; the Ural ЦСУ is a dead end and a new one is coming for the federal project (alive in November, handed over in December).
- Also here: 0:02:04–0:02:18 (lines 17–17) the two sites; 1:00:54–1:01:25 (lines 229–229) the VPN from the site; 2:27:07–2:28:22 (lines 523–527) central firmware updates; 5:25:22–5:26:26 (lines 1153–1157) traps to ЦСУ.

Slides

- 028 1:37:09 «Обзор ЦСУО» (title); 029 1:37:28 «ЦСУО» ★ (two data centres F1/F2, 350+ sites, 5000+ devices); 030 1:38:58 «Компоненты ЦСУО» ★ (re-shown 1:42:09); 031 1:40:36 «Вопросы?».

Follow-ups

- [editorial] central-management.md:91 «на момент проведения лекции»: reword. The content is from 1:43:16.

Vendor-attributed lines: none.

Leads

- central-management.md:76 names «ДЦА». The audio at 1:41:38 has «вместе с ДП … ДП будет готовить конфигурацию и софт», probably РДП. Check by ear.
- Slide 030: 18 components (TRFPRC, LCKLOG, TRFLOG, DEVINV, DEVCTL, REGINT, DEVMON, DEVLOG, SMON, SLOG, IM, REPORT, GISMAP, UAAA, BACKUP, CONFIG, NTP, WIKI; the reserve site lacks LCKLOG and TRFLOG) and the gateways IPC-3000F at ЦСУ and IPC-100 at the sites. 21.4 describes five subsystems.
- Slide 029 names the sites F1 and F2.

Changes from other sessions: none yet.

### 22. Распознавание протоколов и двухстадийная блокировка · docs/protocol-blocking.md

Transcript

- 1:10:33–1:14:50 (lines 259–271) how the protocol lists are formed: the filters recognise and log without blocking and send the logs to СПФС; СПФС passes them to ЦСУ over gRPC; ЦСУ analyses logs from all sites and builds lists (IP and port of Telegram servers and proxies); the lists go back to the filters over HTTP into a separate DPI list, and by BGP to EcoHighway. 1:10:49–1:11:07 is a participant's microphone.
- Q&A 1:43:31–1:47:14 (lines 373–385) list forming for the echelon from the start; the full cycle under 15 min in the Surgut tests (sometimes 5–6), depending on the СПФС and analyser settings; a new proxy works until the filter gets the updated list.
- 2:48:46–2:51:23 (lines 601–607) `debug_logger` to СПФС (home 14.10).
- 3:24:02–3:25:24 (lines 721–725) `behaviour ignore` for recognition, `block` for blocking (home 17.4).
- Q&A 4:00:40–4:02:29 (lines 853–859) protocols named in a list's `protocols` are degraded or blocked at once (home 17.3).
- Q&A 4:10:08–4:16:40 (lines 885–909) recognition by a dozen or more features (addresses, ports, packet frequency, sizes and their variation, keyword frequency, especially for encrypted traffic); false positives, hence the two-step blocking of Telegram (recognise, clean in ЦСУ, load back; the example blocking list is 5); obfuscation: «it depends», cat and mouse, new signatures; several packets in both directions of one session are needed.

Slides

- 025 1:10:33 «Формирование и загрузка списков фильтрации» ★ (re-shown 1:14:55, 1:25:51, 1:44:23); 024 1:09:23 (the FlowSpec text); 064 2:48:44 «Настройка журналирования протоколов»; 075, 077 (`behaviour`).

Follow-ups

- [editorial] Dedupe 22.4 against 22.5–22.10: the «Разделение DPI-листов» table (protocol-blocking.md:140–149) equals the 22.9 table (239–250); «Время полного цикла» (159–161) repeats 22.10; «Преимущества централизованного анализа» (151–157) repeats 22.8; the first paragraph of 22.5 repeats 22.2.
- The recognition list's number is unknown, so call it «лист распознавания»: «А0» at 4:13:41 is garbled, while the blocking-list example 5 is clear (4:14:00). 22.5 «Лист 0 для этого не используется» is an inference that names a number [t, in part]: drop it.
- `behaviour` [slides 075, 077, 087]; `behavior` remains at filter-dpi.md:184, 210; protocol-blocking.md:112, 135, 174, 272; filter-monitoring.md:305.
- 22.1.4 «keywords are useless for encrypted traffic» [contradicted: t 4:10:54–4:11:31 «особенно актуально для шифрованного трафика»].
- 22.2 «прямая блокировка по DPI не применяется» [contradicted in part: Telegram is blocked in two steps (t 4:12:20), but a protocol named in a list's `protocols` is degraded at once (t 4:01:44–4:02:08), as filter.md:162 describes].
- [editorial] «десяток и более» (protocol-blocking.md:13) vs «не один десяток» (filter.md:134); speech at 4:10:48 has «десяток и не один».

Vendor-attributed lines: none.

Leads

- «BGP FlowSpec» (slides 024, 025) is in no chapter. Slide 025: the filters send logs to СПФС over UDP and pull the final lists over HTTP.
- The 22.3 table (protocol-blocking.md:83) says the filter unwraps simple (XOR) obfuscation. That was the asker's premise; the speaker answered «it depends» (4:14:15–4:15:39). The obfuscation named at 4:14:16 is garbled («CMP»).

Changes from other sessions: none yet.

## Part V. Эксплуатация

### 23. Траблшутинг · docs/troubleshooting.md

Transcript (scattered; the home chapter in brackets)

- Q&A 0:35:01–0:36:37 (lines 131–137) which filter holds a session: no logs on the balancer, walk the site's filters (a script does about 15 in 10 s) [23.2; 6.5.4].
- 0:51:08–0:52:02 (lines 191–193) behind CGNAT only white addresses are seen: get the NAT translation from the operator [23.2; home 3.3.1].
- Q&A 1:25:25–1:29:57 (lines 307–323) EcoHighway keeps no logs (real time only); an operator says EcoHighway filters its BGP session: look up the IP and port 179 in the ЦСУ lists, check sessions on the filters, put EcoHighway into software bypass and see whether the problem stays [23.1, 23.3, 23.4; 4.6].
- 2:01:01–2:02:44 (lines 435–441) the subscriber's local IP comes first; Internet addresses on the local side mean a LAN/WAN mix-up [23.6; home 12.5].
- 2:43:11–2:46:10 (lines 581–591) raise `verbose` only for troubleshooting [14.8].
- 3:13:19–3:14:00 (lines 683–685) disabling DPI as a diagnostic [17.1].
- 3:28:25–3:29:42 (lines 735–737) `no_ip` as a diagnostic [23.5; 17.4].
- 3:34:09–3:35:28 (lines 755–759) the S/N from `show version` goes into every support request [18.1].
- Q&A 3:44:31–3:45:55 (lines 791–797) tables at 25–30 %: contact support; more traffic than planned, or a DoS [18.7].
- 3:59:12–4:00:01 (lines 845–849) `show dpimatch` [23.3; home 18.13].
- Q&A 4:07:30–4:08:58 (lines 877–881) RKN registry download failures: below about 10 Mbit/s, interface errors, cured by a reboot [17.2].
- Q&A 4:16:40–4:21:46 (lines 909–927) ping and traceroute only check management; a business subscriber's complaint: no packet crafting, after-the-fact analysis is hard, look for live sessions, check the DPI lists, about 80 % of cases are not ТСПУ; a corporate client can reproduce it live; the filter is L2 and cannot originate traffic [23.1–23.3, 23.7, 23.8].
- 5:10:40–5:11:49 (lines 1099–1103) a bypass rule for the operator's VLAN: if the behaviour changes, dig further; growing counters show «мы ваш трафик видим, но не трогаем» [23.4; 9.5].
- Q&A 5:20:48–5:26:26 (lines 1135–1157) group bypass and the automatic return; whole-site bypass in the Ural pilot vs per group; table load and keep-alives; traps [23.4, 23.7; 6.6].

Slides

- 043, 044 (session search syntax), 087 (`show dpimatch`), 128 (flow counters), 129–130.

Follow-ups

- [editorial] 23.2 «Особенности при установке после CGNAT» (troubleshooting.md:93–95) restates 3.3.1. Keep a link and the practical step: get the NAT address:port from the operator and search by it [t 0:51:41; slides 043, 044 `show sessions lap <ip>:<port>`].
- (found in the check) 23.2 uses `show session la …` / `ra …` [contradicted: `lap`, `rap`, `local`, `remote`, … on slides 043, 044].
- 23.5 `system dpi lists <N> no-ip` (troubleshooting.md:171, 182) → the branch `system dpi dpilist<N>` and the parameter `no_ip` [slides 046, 075]. `no_ip +=(<ip>)` is an inference from the list syntax (slide 053); no slide shows it.
- 23.4 `match vlan 0 id <VLAN>` → `vlan0-tag <VLAN>`; the path is `ecofilter-balancer filters …`; `priority 200` is not «high» [slides 122, 123, 128; t 5:01:20].
- 23.4 and 9.7 `call ecofilter-balancer set-bypass-ecofilter-unit …` [vendor-only; t 5:13:44].

Vendor-attributed lines: none.

Leads

- No section covers escalating to the vendor (what to send and when: the S/N, tables above 20 %, shrinking mbufs, CPU at 80–90 %). Proposed as 23.9 «Обращение в техподдержку», awaiting approval.
- The BGP-session example with port 179 (1:27:43) is not in chapter 23.

Changes from other sessions: none yet.

## Coverage gaps

### Transcript stretches no chapter covers

| Range | Material | Proposed home |
|---|---|---|
| 3:34:09–3:35:28, 3:44:31–3:48:11 | When and how to contact vendor support: the S/N in every request; triggers (tables above 20 %, shrinking mbufs, CPU 80–90 %). The agenda's «Обращение в техподдержку» was never presented. | 23.9 «Обращение в техподдержку» (proposed); items for 24 |
| 1:31:47–1:35:02 | Echelon design and scaling: jumper capacity, one LAG per balancer, design inputs, the «EHW or not» field in the balancer design template, sizing with the type-A figures | 4.8 «Проектирование эшелона» (proposed; 6.3.3 keeps the type-A side) |
| 4:39:27–4:41:46 | Connecting to the balancer (serial 9600 (38400) 8N1, SSH 22), the CLI command tables, the configuration tree with NTP and TACACS | 7.5 (connection); 8.1 (commands, tree); 8.10 (NTP, TACACS; proposed) |
| 5:18:30–5:19:30 | `bypass-watchdog-groups` status (GL Sun) | 9.8 (proposed; now an unnumbered sub-heading in 9.7) |
| 4:25:15–4:27:00 | The filter's IPMI port vs its log ports | 11.4; 20.4 |
| 3:17:07–3:17:41 | DPI `shortlist` | 17.1 |
| 2:48:46–2:51:23 (part) | The unused `protocol_log` block | 14.10 |
| 2:56:07–2:58:42 (parts) | `alg`, `udp_inbound_refresh` and three NAT-only parameters | 15.2 |
| whole lecture | Values the slides mark as mandatory (vlan_mode qinq, forward_traffic on, l2mtu 9216, lldp off, permit_invalid_flow on, a fake pool with acl and enable, IPv6 on, DPI on, send_rst off, functionality_mode normal_nat, whitelist_mode off, update_schedule not never, debug_logger with 3 packets via LOG, autologoff not never, TACACS fallback on) and the balancer example configuration (slides 119–124) | 24 «Типовая конфигурация (чек-лист)» |
| whole lecture | Terms: АСБИ, ТСПУ тип А/Б, ЦСУО, СПФС, СПХД, BMC/IPMI, LAN/WAN, линк, flow, balance group / filter group, heartbeat vs keep-alive, Inline/TAP/Active/Passive Bypass, программный байпас, on-a-stick, pipeline, перемычка, TCAM, FlowSpec, the EcoSGE licences, сессия/трансляция, lap/gap/rap, DDM, mbuf, CPS, Optimal, control/data plane, ГРФЦ, QinQ, LLDP, ALG, hairpin, DPDK, SNI, QUIC, TACACS+, «мышеловка», startup/effective/lastapply/factory, tries/stable/Factory | 25 «Глоссарий» |

### Slides no chapter uses

| Slide | Content | Proposed home |
|---|---|---|
| 024, 025 | «BGP FlowSpec» | 4.3.1; 22.9 |
| 030 | 18 ЦСУО components; IPC-3000F / IPC-100 | 21.4 |
| 050 | `copy hwinfo` (not spoken) | 19.3 |
| 085 | Log record format and levels | 18.12 |
| 115 | Balancer connection settings | 7.5 |
| 116, 117 | Balancer CLI tables and tree | 8.1 |
| 023 | Type-B site topology ★ | 4.3 |
| 001 | Agenda (the lecture plan) | none: chapters don't mirror the lecture |
| 002, 021, 028, 032, 110 | Section titles with device photos | none; 033 and 111 have better photos |
| 031, 089, 109, 131, 132 | «Вопросы?» | none |
| 090–108 | Flips back through earlier slides | covered by their originals |

### Organisational stretches (nothing to cover)

0:00:00–0:00:51 agenda; 0:03:10–0:03:32 drawing check; 0:20:22–0:20:40 aside about a separate bypass course; 0:29:40–0:30:07; 0:57:31–0:57:39; 1:01:25–1:01:55; 1:10:49–1:11:07 microphone; 1:25:11–1:25:25; 1:40:36–1:41:12 break; 2:08:19–2:08:49; 2:48:40–2:48:46; 3:43:45–3:44:31 lunch-break talk; 4:00:22–4:00:40; 4:21:46–4:22:29 chat and a reconnect; 4:27:00–4:28:23 a forgotten question (never asked) and the break; 5:19:30–5:19:42. The recording ends at 5:26:26, mid-answer.

## Boundary corrections against the memory map

Checked against the word timings. Unchanged (within 6 s): 0:09:38, 0:13:49, 0:29:40, 0:42:36, 0:44:37, 0:48:43, 0:57:31, 0:57:39, 1:01:55, 1:10:33, 1:14:50, 1:16:06, 1:25:11, 1:37:09, 1:40:36, 1:47:14, 1:55:29, 2:12:49, 2:22:39, 2:28:22, 2:31:30, 2:34:25, 2:48:40, 2:51:23, 2:54:01, 3:03:27, 3:11:00, 3:12:02, 3:34:09, 3:43:51–3:44:31, 4:00:22, 4:10:12, 4:16:39, 4:21:45, 4:27:45–4:28:21, 4:30:17, 4:34:17, 5:03:39, 5:05:50, 5:18:30, 5:20:48, 5:23:51.

| Chapter | Memory map | Now | Why |
|---|---|---|---|
| 1 overview | 0:00:01–0:09:38 | 0:00:51–0:09:38 | 0:00:00–0:00:51 is the agenda |
| 5 bypass | 0:13:49–0:20:40 | 0:13:49–0:20:22 | 0:20:22–0:20:40 is an aside about a separate bypass course |
| 6 balancer | 0:20:40–0:48:37 as one block | 0:20:40–0:42:27 and 0:44:40–0:48:37 | 0:42:36–0:44:37 is the filter path (chapter 10) |
| 23 troubleshooting | Q&A 1:25:11–1:37:09 | 1:25:25–1:29:57 | the rest of that Q&A is the echelon path, sizing and history (chapter 4) |
| 21 central-management | Q&A 1:41:12–1:47:14 | 1:41:12–1:43:31 | 1:43:31–1:47:14 is list forming and the blocking cycle |
| 22 protocol-blocking | — | adds 1:43:31–1:47:14 | the source of 22.10 (5–15 min) |
| 16 filter-acl-pools | 3:03:27–3:11:00 | 3:03:30–3:09:59 | 3:09:59–3:11:00 is the `/ipv6` section |
| 15 filter-interfaces | 2:51:23–3:03:27 | adds 3:09:59–3:11:00 | the `/ipv6` section belongs to 15.4 |
| 11 filter-platform | Q&A 4:21:59–4:27:00 | 4:22:29–4:27:00 | 4:21:46–4:22:29 is the chat and a reconnect |
| 7 / 8 | 7 ends and 8 starts at 4:40:54 | 4:40:28 | the CLI modes and `edit` (slide 116) belong to 8.1 |
| 23 troubleshooting | four stretches | adds 0:35:01, 0:51:08, 1:25:25, 2:01:01, 3:13:19, 3:28:25, 3:59:12, 4:07:30, 5:10:40 | troubleshooting asides the memory map missed |
| 5 bypass | five stretches | adds 4:33:46, 4:55:09, 5:20:48 | the GL Sun and Ural-bypass asides |
| 20 management-segment | one stretch | adds 4:25:15–4:27:00 | IPMI vs log subnets |
| 12 filter-sessions | one stretch | adds 0:35:01–0:36:37 | finding a session's filter |

## Recurring recognition errors

For reading the transcript. The wrong forms that reached the docs are in validate.py (`TERMS`), which reports each one as a `terms` warning.

| Transcript | Meant |
|---|---|
| ТСКУ, ТСУ, ДСПУ, ску, теску | ТСПУ |
| СБИ, ASBI | АСБИ |
| ЦСО | ЦСУ / ЦСУО |
| шалонированная, шланированная, эшелок | эшелонированная, эшелон |
| e highway, экохавей, eкохай | EcoHighway |
| экофильтрбалансер | EcoFilter-Balancer |
| онстик, он стик, монстико | on-a-stick |
| лампорт, oneпорт, «в сторону One» | LAN-порт, WAN-порт, WAN |
| ЦГНАТ, циганат, Цигнат | CGNAT |
| киплайв, KLI, KPI-пакет | keep-alive |
| карбит, хардбит | heartbeat |
| Silликом, силикон | Silicom |
| GLS, JIL Sun, JLSN | GL Sun (GLSUN) |
| TPI, движок TPI | DPI |
| behavor | `behaviour` |
| P41, B42 | `p4-1`, `p4-2` |
| balancing s Mac | `balancing-as mag-hash` |
| N UnitQA | `nat-unit-queues` |
| Vant 1, VN ID | `vlan0-tag 1` |
| show XL | `show xlate` |
| la, LAAB | `lap` |
| show counters div | `show counters diff` |
| shows | `show logs` |
| Times Q, ESQ | `timeskew` |
| FB on | `fallback on` |
| Firm Reвеt | `firmware revert` |
| Van Mode, KnQ | `vlan_mode`, `qinq` |
| WH list mode | `whitelist_mode` |
| loges of on | `log_matches` |
| Аckк clickли list | `quic_list` |
| КПСТИ, пенси | `capacity` |
| call rdp install | `call rdp-firmware install from-file` |
| шоу RDP firm | `show rdp-firmware` |
| 314040 BP | `3.1.4.0.40.bp` |
| SS, «админ собака» | `ssh admin@` |
| «ДП» (1:41:38) | probably РДП |
| «А0» (4:13:41) | unresolved; don't name the list |
| «CMP» (4:14:16) | unresolved obfuscation name |
