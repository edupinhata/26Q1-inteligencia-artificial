\section*{Resumo}

%Este artigo\cite{mittalResponsibleMachineLearning2024} levanta a questão da integridade e confiabilidade das bases de dados utilizados para treinamento dos modelos de Inteligência Artificial. Para isso, ele avalia as bases de dados pelas lentes de \textbf{equidade}, \textbf{privacidade} e \textbf{conformidade regulamentar}. Os autores também fazem uma avaliação de um grande conjunto de bases de dados de visão computacional. Eles focam a discussão em bases de dados de biometria e assistência médica, entretanto garantem que os métodos de análise apresentados podem ser estendidos para outras bases de dados.

Os avanços atuais em Inteligência Artificial tem impactado bilhões de vidas em diversas áreas. Esse avanço tem feito com que, a cada dia, melhores padrões de acurácia sejam alcançados. Em diversas áreas a IA consegue ultrapassar especialistas em diagnósticos e jogos complexos.
A melhoria da acurácia nos métodos de IA é muito influenciada pelos dados coletados e as anotações atribuídas à esses dados. E apesar da sua importância para os resultados obtidos, a qualidade dos dados geralmente permanece subestimada na comunidade de Inteligência Artificial e Aprendizado de máquina.

Este artigo\cite{mittalResponsibleMachineLearning2024} levanta a questão da integridade e confiabilidade das bases de dados utilizadas para treinamento dos modelos de Inteligência Artificial.

Os autores apontam diversos estudos para melhorar quantitativamente e qualitativamente os dados, como criar fichas técnicas detalhadas para as bases de dados já criadas, estudos qualitativos de como documentar contextos em imagens de bases de dados, frameworks institucionais e procedimentos inspirados em arquivologia para lidar com consentimento, inclusividade e preocupações de privacidade. Diversos outros estudos nesse sentido foram analisados, entretanto, poucos desses artigos examinaram as dimensões de equidade, privacidade e conformidade regulamentar. Os autores deste artigo então utilizaram conceitos de valores éticos de IA para apresentar uma auditoria de diversas bases de dados de visão computacional focando em \textbf{equidade}, \textbf{privacidade} e \textbf{conformidade regulamentares}.

Para \textbf{equidade}, os autores focaram no impacto de três fatores para quantificar uma base de dados \textbf{justa}: 

\begin{itemize}
\item \textbf{inclusividade}: quantifica os diferentes grupos de pessoas representadas na base de dados, considerando gênero, cor de pele, etinicidade e idade. 
\item \textbf{diversidade}: quantifica a distribuição dos grupos considerados na inclusividade dentro da base de dados.
\item \textbf{rótulos:} tem valores diferentes dependendo se os rótulos foram autodeclarados pelos indivíduos representados na base de dados, ou se foram rotulados baseados em características aparentes.
\end{itemize}

Os autores ressaltam que uma base de dados balanceada não garante uma performance igual, entretanto usar uma base de dados mais balanceada melhora a equidade.

Para quantificar \textbf{privacidade}, foram identificados rótulos sensíveis que podem potencialmente causar vazamento de informações privadas. Foram observados seis atributos mais comumente usados: identificação por nome, atributos sensíveis, acessórios, objetos críticos, inferência de localização e condição médica.

Para quantificar \textbf{conformidade regulamentar}, foram utilizados três fatores: aprovação institucional, consentimento do indivíduo na coleta de dados, facilidade de remover/corrigir dados do usuário na base de dados.

Depois de definir como quantificar, eles analisaram 100 bases de dados. Dentre essas, algumas não puderam ser acessadas, restando 60 bases de dados, dentre as quais 52 são base de dados de biometria facial e oito são bases de dados de raio-X de tórax. Quantificaram todas essas bases de dados pelas dimensões de equidade, privacidade e conformidade regulamentar. E observaram os seguintes pontos:
\begin{itemize}
\item a maioria das bases de dados tem problemas nos três fatores;
\item apesar de muito dos trabalhos afirmarem que essas bases de dados focam em equidade, os valores de equidade encontrados neste estudo foram baixos;
\item grande número de base de dados de larga escala em visão computacional foram obtidas pela Internet sem nenhuma aprovação institucional;
\item Apesar de seguir normas regulamentares melhora o conjunto de critérios para montar uma base de dados, a maioria das bases não deixa claro se estão de acordo com normas e aprovações éticas;
\item Ao comparar a pontuação entre equidade, privacidade e conformidade regulamentar, em geral privacidade possui maior nota.
\end{itemize}

Enfim, os resultados evidenciam a necessidade de uma revisão das metodologias de criação de bases de dados, dado os avanços nas legislações de proteção de dados. Os próprios autores dizem que o método de auditoria que propuseram ainda tem alguns problemas, como por exemplo o paradoxo da equidade-privacidade, em que aumentar a equidade tende a diminuir a privacidade pelo aumento da quantidade de dados potencialmente sensíveis, e vice-versa. Mesmo com essas limitações, os autores foram efetivos em apresentar uma metodologia para avaliar bases de dados de aprendizado de máquina sob as dimensões de equidade, privacidade e conformidade regulamentar.