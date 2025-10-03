# LabelImg Compatibility Fixes (Python 3.11 / PyQt)

This project uses LabelImg for image annotation, but recent versions of Python and PyQt enforce stricter type requirements that cause LabelImg to crash. Below are the manual fixes applied to ensure compatibility.

## 🔧 Files Modified

| File Location                                                                 | Purpose of Change                              | Line(s) Modified |
|-------------------------------------------------------------------------------|------------------------------------------------|------------------|
| `.venv/lib/python3.11/site-packages/labelImg/labelImg.py`                    | Fixed scroll bar type mismatch (`setValue`)    | Line 965         |
| `.venv/lib/python3.11/site-packages/libs/canvas.py`                          | Fixed drawing type mismatches (`drawLine`, `drawRect`) | Lines 526, 530, 531  |

## 🛠️ Fixes Applied

### 1. `labelImg.py` — Scroll Bar Crash
**Before:**
bar.setValue(bar.value() + bar.singleStep() * units)

**After:**
bar.setValue(int(bar.value() + bar.singleStep() * units))

### 2. `canvas.py` - Drawing Box errors
**Before:**
[526] p.drawLine(self.prev_point.x(), 0, self.prev_point.x(), self.pixmap.height())
[530] p.drawRect(left_top.x(), left_top.y(), rect_width, rect_height)
[531] p.drawLine(0, self.prev_point.y(), self.pixmap.width(), self.prev_point.y())

**After:**
[526] p.drawLine(int(self.prev_point.x()), 0, int(self.prev_point.x()), int(self.pixmap.height()))
[530] p.drawRect(int(left_top.x()), int(left_top.y()), int(rect_width), int(rect_height))
[531] p.drawLine(0, int(self.prev_point.y()), int(self.pixmap.width()), int(self.prev_point.y()))