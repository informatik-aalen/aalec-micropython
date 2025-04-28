"""Beeper constants."""

from micropython import const  # type: ignore


# Predefined frequencies of tones for the beeper
t_off: int = const(0)
"""Frequency off"""
t_c_1: int = const(262)
"""Frequency of the tone C1"""
t_d_1: int = const(294)
"""Frequency of the tone D1"""
t_e_1: int = const(330)
"""Frequency of the tone E1"""
t_f_1: int = const(349)
"""Frequency of the tone F1"""
t_g_1: int = const(392)
"""Frequency of the tone G1"""
t_a_1: int = const(440)
"""Frequency of the tone A1"""
t_h_1: int = const(494)
"""Frequency of the tone H1"""
t_c_2: int = const(523)
"""Frequency of the tone C1"""
t_a_2: int = const(880)
"""Frequency of the tone A2"""

DUTY50: int = const(512)
"""50% duty cycle"""
