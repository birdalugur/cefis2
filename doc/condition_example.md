```python
import pandas as pd
import src.condition as condition
```

## Örnek Veri


```python
data = pd.read_excel('example_data.xlsx')
data
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>duration</th>
      <th>amplitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2018-09-06 00:00:17</td>
      <td>00:00:13</td>
      <td>-2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2018-09-06 00:00:39</td>
      <td>00:00:22</td>
      <td>3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2018-09-06 00:00:48</td>
      <td>00:00:09</td>
      <td>-1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2018-09-06 00:00:49</td>
      <td>00:00:01</td>
      <td>4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2018-09-06 00:00:50</td>
      <td>00:00:01</td>
      <td>-7</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2018-09-06 00:00:51</td>
      <td>00:00:01</td>
      <td>7</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2018-09-06 00:00:53</td>
      <td>00:00:02</td>
      <td>-9</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2018-09-06 00:01:01</td>
      <td>00:00:08</td>
      <td>7</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2018-09-06 00:01:04</td>
      <td>00:00:03</td>
      <td>-11</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2018-09-06 00:01:05</td>
      <td>00:00:01</td>
      <td>5</td>
    </tr>
    <tr>
      <th>10</th>
      <td>2018-09-06 00:01:17</td>
      <td>00:00:12</td>
      <td>-2</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2018-09-06 00:01:21</td>
      <td>00:00:04</td>
      <td>8</td>
    </tr>
    <tr>
      <th>12</th>
      <td>2018-09-06 00:01:22</td>
      <td>00:00:01</td>
      <td>-1</td>
    </tr>
    <tr>
      <th>13</th>
      <td>2018-09-06 00:01:24</td>
      <td>00:00:02</td>
      <td>2</td>
    </tr>
    <tr>
      <th>14</th>
      <td>2018-09-06 00:02:11</td>
      <td>00:00:47</td>
      <td>-9</td>
    </tr>
    <tr>
      <th>15</th>
      <td>2018-09-06 00:02:31</td>
      <td>00:00:20</td>
      <td>6</td>
    </tr>
    <tr>
      <th>16</th>
      <td>2018-09-06 00:02:35</td>
      <td>00:00:04</td>
      <td>-16</td>
    </tr>
    <tr>
      <th>17</th>
      <td>2018-09-06 00:04:01</td>
      <td>00:01:26</td>
      <td>4</td>
    </tr>
    <tr>
      <th>18</th>
      <td>2018-09-06 00:04:07</td>
      <td>00:00:06</td>
      <td>-2</td>
    </tr>
    <tr>
      <th>19</th>
      <td>2018-09-06 00:04:12</td>
      <td>00:00:05</td>
      <td>19</td>
    </tr>
  </tbody>
</table>
</div>



## Medyana göre işlem yapmak için


```python
signs=condition.Sign(data).medyan()
```

    duration= {'pozitif': 4.5, 'negatif': nan}
    amplitude= {'pozitif': 5.5, 'negatif': -4.5}
    


```python
condition.apply(data,signs)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>duration</th>
      <th>amplitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2018-09-06 00:00:17</td>
      <td>00:00:13</td>
      <td>-2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2018-09-06 00:00:39</td>
      <td>00:00:22</td>
      <td>3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2018-09-06 00:00:50</td>
      <td>00:00:11</td>
      <td>-4</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2018-09-06 00:00:51</td>
      <td>00:00:01</td>
      <td>7</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2018-09-06 00:00:53</td>
      <td>00:00:02</td>
      <td>-9</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2018-09-06 00:01:01</td>
      <td>00:00:08</td>
      <td>7</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2018-09-06 00:01:17</td>
      <td>00:00:16</td>
      <td>-8</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2018-09-06 00:01:21</td>
      <td>00:00:04</td>
      <td>8</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2018-09-06 00:02:11</td>
      <td>00:00:50</td>
      <td>-8</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2018-09-06 00:02:31</td>
      <td>00:00:20</td>
      <td>6</td>
    </tr>
    <tr>
      <th>10</th>
      <td>2018-09-06 00:02:35</td>
      <td>00:00:04</td>
      <td>-16</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2018-09-06 00:04:01</td>
      <td>00:01:26</td>
      <td>4</td>
    </tr>
    <tr>
      <th>12</th>
      <td>2018-09-06 00:04:07</td>
      <td>00:00:06</td>
      <td>-2</td>
    </tr>
    <tr>
      <th>13</th>
      <td>2018-09-06 00:04:12</td>
      <td>00:00:05</td>
      <td>19</td>
    </tr>
  </tbody>
</table>
</div>



## Percentile'a göre


```python
signs=condition.Sign(data).percentile(.7)
```

    duration= {'pozitif': 9.899999999999997, 'negatif': nan}
    amplitude= {'pozitif': 7.0, 'negatif': -2.0}
    


```python
condition.apply(data,signs)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>duration</th>
      <th>amplitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2018-09-06 00:00:17</td>
      <td>00:00:13</td>
      <td>-2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2018-09-06 00:00:39</td>
      <td>00:00:22</td>
      <td>3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2018-09-06 00:01:17</td>
      <td>00:00:38</td>
      <td>-7</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2018-09-06 00:01:21</td>
      <td>00:00:04</td>
      <td>8</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2018-09-06 00:02:11</td>
      <td>00:00:50</td>
      <td>-8</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2018-09-06 00:02:31</td>
      <td>00:00:20</td>
      <td>6</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2018-09-06 00:02:35</td>
      <td>00:00:04</td>
      <td>-16</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2018-09-06 00:04:01</td>
      <td>00:01:26</td>
      <td>4</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2018-09-06 00:04:07</td>
      <td>00:00:06</td>
      <td>-2</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2018-09-06 00:04:12</td>
      <td>00:00:05</td>
      <td>19</td>
    </tr>
  </tbody>
</table>
</div>


