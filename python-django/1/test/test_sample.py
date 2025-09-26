from unittest import TestCase

from solution import queranumeric


class QueranumericTests(TestCase):
    def test_1(self):
        order = 'DL?!'
        words = [
            '!L?D!DD?!?', 
            'L?DL?DLLDD', 
            'LD????DD!!?L',
        ]
        expected = [
            'LD????DD!!?L',
            'L?DL?DLLDD',
            '!L?D!DD?!?',
        ]
        actual = queranumeric(order, words)
        self.assertEqual(actual, expected)

    def test_2(self):
        order = '!%Oyz['
        words = [
            'OzO![%yz[O!%!',
            'y%[!y%OyzzOy!',
            '!yOy!!z[O[O%z[O[zyO![zO',
            '![[z!%Oyyzzzy!zzOO![!',
            'z[[OyO![Oy!yz[!y[O',
            '%[[[y!!z%yO[zzOy!!O'
        ]
        expected = [
            '!yOy!!z[O[O%z[O[zyO![zO',
            '![[z!%Oyyzzzy!zzOO![!',
            '%[[[y!!z%yO[zzOy!!O',
            'OzO![%yz[O!%!',
            'y%[!y%OyzzOy!',
            'z[[OyO![Oy!yz[!y[O'
        ]
        actual = queranumeric(order, words)
        self.assertEqual(actual, expected)

    def test_3(self):
        order = '"%tF!nME*'
        words = [
            '"MnM*nE"M',
            'FM**EMnn*%**FM"M',
            '%E"FE**"%',
            '!FtF*EtE%n""%"n"*n!%"FtM',
            '"t*ttMnnnE"!E%*Fn!ttt"EFF%%M!n',
            '"%"E%"**nnn*M!%%t!M%t!EtnME!Fn*"M',
            '%E"t*M%nn*',
            '*M!%!n',
            'nFEF!%MF*%"!n!!'
        ]
        expected = [
            '"%"E%"**nnn*M!%%t!M%t!EtnME!Fn*"M',
            '"t*ttMnnnE"!E%*Fn!ttt"EFF%%M!n',
            '"MnM*nE"M',
            '%E"t*M%nn*',
            '%E"FE**"%',
            'FM**EMnn*%**FM"M',
            '!FtF*EtE%n""%"n"*n!%"FtM',
            'nFEF!%MF*%"!n!!',
            '*M!%!n'
        ]
        actual = queranumeric(order, words)
        self.assertEqual(actual, expected)

    def test_4(self):
        order = 'I6vz;L&>W"mgbd^'
        words = [
            '>&I^"dz&>gzz;&L;6zbLLLW&I&',
            'd;^;66IW"mdd;"6L"vz;I6Lz',
            '&zd^>;6Izmg"dLvdLWgb"W^W>"^>L&&"6',
            ';z>&b6gzIId>W6W&&m6^v>Lbdv>&Wdbb;z>L;m',
            'zzW^>gg>b;"d^&"6LW;',
            'bdgddW"',
            '>WvWI>WL&>m',
            '^dv&IgIgg;&">6dm";m&W&W',
            'b&mWz6IWvIz^zbm',
            '^>dL;d^m',
            'dzz6;m"zL&vLzdmgm6vg>'
        ]
        expected = [
            'zzW^>gg>b;"d^&"6LW;',
            ';z>&b6gzIId>W6W&&m6^v>Lbdv>&Wdbb;z>L;m',
            '&zd^>;6Izmg"dLvdLWgb"W^W>"^>L&&"6',
            '>&I^"dz&>gzz;&L;6zbLLLW&I&',
            '>WvWI>WL&>m',
            'b&mWz6IWvIz^zbm',
            'bdgddW"',
            'dzz6;m"zL&vLzdmgm6vg>',
            'd;^;66IW"mdd;"6L"vz;I6Lz',
            '^>dL;d^m',
            '^dv&IgIgg;&">6dm";m&W&W'
        ]
        actual = queranumeric(order, words)
        self.assertEqual(actual, expected)

    def test_5(self):
        order = 'xv@C-h)7QX9zy_Y`P}f"6'
        words = [
            'yvCQQ`6}7xYh_PXfP)xYC@h`6x-9y_v7Qyz}PC}_6C)CPXhz9"X_-69hY)P-',
            'z7""y}vvYvXz}6C-"_`Q"YY@`P`--6fXzx69P-z@Y_-ChXxv}7h7"`xfPfX7XYC7x_"y',
            'P6@`@hxyh7P_-YPx`PCx"")Xz)}Cx@7hxvQP)x}Y-)C_h-7_yP"`_66',
            'vf7X6`7)}yx6QQy9P_YhQy`xQ@)Y76hvX)_"-67h"7@)}--',
            'Y)hxf9Yh-7_x"@X)vyC9)@xfP-xP)z',
            '-_PQQYQv-Q)"yfyxyy_`"`_@X',
            'hQxzXXPY7"6xz}PC"_fC',
            'f"}""y7vhhvQhYxCf}Q"@6zYfC96))`xXQff)XXf',
            'C@96Ch6x}x6`f"9v@@h79x767)vhx@X-fxyvv-"yfX-Yh_xvYhxyf}Pzz)97"CfCX6hfCzXx`PxC9Y',
            ')79"XhX7XP_6}-Yhyvy"-YQ7z`Pz"CyXxQzf-_97XY_yC76z-`CX"CPvX--x"-x@Q}`7-`',
            '--`99C7Py@)7Q7fC-C7yz"67fY7)zv}_9P)yz_@C6"@zv-fQfh9hPy@`Xxhx@QX}xC',
            '_@9_}-6xh`}h)6y9``-9hXvyQ"x9XQ_v6fC)C_97`QC}hx@-9Q}}"yz"hC66PC',
            '"_77@)fQX',
            '_hzfYv99`Q79f@"799xzQ_v}"@v9PY6PX@_Q7zh997Y)9X)Q-y_-X-`"6',
            '9Q@h7v6XQ)YYY`Py6fCQ_xQY}@Yf""_vC_v@Y7-P}@9Q@`fx99X)Y}z)z9',
            'Px)6-)y``"xxfCx}XX9Q`y7-XvYQ)zf6}9x`YzC7X7`P}Pf9-ChzCz',
            'z-f@@-_Xf)-_xvPfChzh)XP`_-Px}xyP@vzQv`fy-9-9@C@y_}Q_fh}yY7X`)hx7P)hPy`x`yX9fv',
            'h66f6P-@"XYXf677C6)X}"z)9yP_h`9)C_h"fxff7"}@9Y)YC}6YxyPC7_',
            'v-X@fQ-`-_P6Q}}"-9)C"76yY_PQX-CQX@"---z9z@}Q9YPYY}_C}YQ6}hY7XQ9_f7)@Y6v"`_)_',
            'vQ}-XxXzY7@6Qf))9PP_vzX-}6"yhy6y@7X}Q`_-)z-6"99y"Xv_fXhh_)_'
        ]
        expected = [
            'v-X@fQ-`-_P6Q}}"-9)C"76yY_PQX-CQX@"---z9z@}Q9YPYY}_C}YQ6}hY7XQ9_f7)@Y6v"`_)_',
            'vQ}-XxXzY7@6Qf))9PP_vzX-}6"yhy6y@7X}Q`_-)z-6"99y"Xv_fXhh_)_',
            'vf7X6`7)}yx6QQy9P_YhQy`xQ@)Y76hvX)_"-67h"7@)}--',
            'C@96Ch6x}x6`f"9v@@h79x767)vhx@X-fxyvv-"yfX-Yh_xvYhxyf}Pzz)97"CfCX6hfCzXx`PxC9Y',
            '--`99C7Py@)7Q7fC-C7yz"67fY7)zv}_9P)yz_@C6"@zv-fQfh9hPy@`Xxhx@QX}xC',
            '-_PQQYQv-Q)"yfyxyy_`"`_@X',
            'hQxzXXPY7"6xz}PC"_fC',
            'h66f6P-@"XYXf677C6)X}"z)9yP_h`9)C_h"fxff7"}@9Y)YC}6YxyPC7_',
            ')79"XhX7XP_6}-Yhyvy"-YQ7z`Pz"CyXxQzf-_97XY_yC76z-`CX"CPvX--x"-x@Q}`7-`',
            '9Q@h7v6XQ)YYY`Py6fCQ_xQY}@Yf""_vC_v@Y7-P}@9Q@`fx99X)Y}z)z9',
            'z-f@@-_Xf)-_xvPfChzh)XP`_-Px}xyP@vzQv`fy-9-9@C@y_}Q_fh}yY7X`)hx7P)hPy`x`yX9fv',
            'z7""y}vvYvXz}6C-"_`Q"YY@`P`--6fXzx69P-z@Y_-ChXxv}7h7"`xfPfX7XYC7x_"y',
            'yvCQQ`6}7xYh_PXfP)xYC@h`6x-9y_v7Qyz}PC}_6C)CPXhz9"X_-69hY)P-',
            '_@9_}-6xh`}h)6y9``-9hXvyQ"x9XQ_v6fC)C_97`QC}hx@-9Q}}"yz"hC66PC',
            '_hzfYv99`Q79f@"799xzQ_v}"@v9PY6PX@_Q7zh997Y)9X)Q-y_-X-`"6',
            'Y)hxf9Yh-7_x"@X)vyC9)@xfP-xP)z',
            'Px)6-)y``"xxfCx}XX9Q`y7-XvYQ)zf6}9x`YzC7X7`P}Pf9-ChzCz',
            'P6@`@hxyh7P_-YPx`PCx"")Xz)}Cx@7hxvQP)x}Y-)C_h-7_yP"`_66',
            'f"}""y7vhhvQhYxCf}Q"@6zYfC96))`xXQff)XXf',
            '"_77@)fQX',
        ]
        actual = queranumeric(order, words)
        self.assertEqual(actual, expected)
