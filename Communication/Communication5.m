
N = 10^6; % number of bits or symbols 
Eb_N0_dB = [0:25]; % multiple Eb/N0 values 
nRx=2;
for ii = 1:length(Eb_N0_dB)
    % Transmitter
    ip = rand(1,N)>0.5; % generating 0,1 with equal probability 
    s = 2*ip-1; % BPSK modulation 0 -> -1; 1 -> 0
    % Alamouti STBC 
    sCode = zeros(2,N);
    sCode(:,1:2:end) = (1/sqrt(2))*reshape(s,2,N/2); % [x1 x2 ...] 
    sCode(:,2:2:end) = (1/sqrt(2))*(kron(ones(1,N/2),[-1;1]).*flipud(reshape(conj(s),2,N/2))); % [-x2* x1*	]
    h = 1/sqrt(2)*[randn(1,N) + 1i*randn(1,N)]; % Rayleigh channel 
    hMod = kron(reshape(h,2,N/2),ones(1,2)); % repeating the same channel for two symbols
    n = 1/sqrt(2)*[randn(1,N) + 1i*randn(1,N)]; % white gaussian noise, 0dB variance
    % Channel and noise Noise addition
    y = sum(hMod.*sCode,1) + 10^(-Eb_N0_dB(ii)/20)*n;

    % Receiver
    yMod = kron(reshape(y,2,N/2),ones(1,2)); % [y1 y1 ... ; y2 y2 ...]
    yMod(2,:) = conj(yMod(2,:)); % [y1 y1 ... ; y2* y2*...]
    % forming the equalization matrix 
    hEq = zeros(2,N);
    hEq(:,[1:2:end]) = reshape(h,2,N/2); % [h1 0 ... ; h2 0...]
    hEq(:,[2:2:end]) = kron(ones(1,N/2),[1;-1]).*flipud(reshape(h,2,N/2)); % [h1 h2 ... ; h2 -h1 ...]
    hEq(1,:) = conj(hEq(1,:)); %   [h1* h2* ... ; h2 -h1	]
    hEqPower = sum(hEq.*conj(hEq),1);
    yHat = sum(hEq.*yMod,1)./hEqPower; % [h1*y1 + h2y2*, h2*y1 -h1y2*,	]
    yHat(2:2:end) = conj(yHat(2:2:end));
    % receiver - hard decision decoding 
    ipHat = real(yHat)>0;
    % counting the errors
    nErr(ii) = size(find([ip- ipHat]),2); 
end
for ii = 1:length(Eb_N0_dB)

    n = 1/sqrt(2)*[randn(2,N) + 1i*randn(2,N)]; % white gaussian noise, 0dB variance

    h = 1/sqrt(2)*[randn(2,N) + 1i*randn(2,N)]; % Rayleigh channel
    % Channel and noise Noise addition 
    sD = kron(ones(2,1),s);
    y = h.*sD + 10^(-Eb_N0_dB(ii)/20)*n;

    % equalization with equal gain combining
    yHat = y.*exp(-1i*angle(h)); % removing the phase of the channel 
    yHat = sum(yHat,1); 
    % adding values from all the receive chains

    % receiver - hard decision decoding 
    ipHat = real(yHat)>0;

    % counting the errors
    nErr1(ii) = size(find([ip- ipHat]),2);

end
for ii = 1:length(Eb_N0_dB)
    % Transmitter
    ip = rand(1,N)>0.5; % generating 0,1 with equal probability 
    s = 2*ip-1; % BPSK modulation 0 -> -1; 1 -> 0
    % Alamouti STBC
    sCode = 1/sqrt(2)*kron(reshape(s,2,N/2),ones(1,2)) ;

    % channel
    h = 1/sqrt(2)*[randn(nRx,N) + 1i*randn(nRx,N)]; % Rayleigh channel 
    n = 1/sqrt(2)*[randn(nRx,N) + 1i*randn(nRx,N)]; % white gaussian noise, 0dB variance 
    y = zeros(nRx,N);
    yMod = zeros(nRx*2,N); 
    hMod = zeros(nRx*2,N); 
    for kk = 1:nRx
        hMod = kron(reshape(h(kk,:),2,N/2),ones(1,2)); % repeating the same channel for two symbols
        hMod = kron(reshape(h(kk,:),2,N/2),ones(1,2)); 
        temp = hMod;
        hMod(1,[2:2:end]) = conj(temp(2,[2:2:end]));
        hMod(2,[2:2:end]) = -conj(temp(1,[2:2:end]));
        % Channel and noise Noise addition
        y(kk,:) = sum(hMod.*sCode,1) + 10^(-Eb_N0_dB(ii)/20)*n(kk,:);
        % Receiver
        yMod([2*kk-1:2*kk],:) = kron(reshape(y(kk,:),2,N/2),ones(1,2));

        % forming the equalization matrix 
        hEq([2*kk-1:2*kk],:) = hMod;
        hEq(2*kk-1,[1:2:end]) = conj(hEq(2*kk-1,[1:2:end]));

        hEq(2*kk, [2:2:end]) = conj(hEq(2*kk, [2:2:end])); 
    end
    % equalization
    hEqPower = sum(hEq.*conj(hEq),1);
    yHat = sum(hEq.*yMod,1)./hEqPower; % [h1*y1 + h2y2*, h2*y1 - h1y2*, ... ]
    yHat(2:2:end) = conj(yHat(2:2:end));
    % receiver - hard decision decoding 
    ipHat = real(yHat)>0;
    % counting the errors
    nErr2(ii) = size(find([ip- ipHat]),2); 
end
simBer = nErr/N; 
simber = nErr1/N; 
simBER = nErr2/N; 
figure
semilogy(Eb_N0_dB,simBer,'ro-','LineWidth',2); 
hold on
semilogy(Eb_N0_dB,simber,'bp-','LineWidth',2); 
semilogy(Eb_N0_dB,simBER,'gd-','LineWidth',2); 
legend('sim(nTx=2,nRx=1,Alamouti)','sim(nTx=1,nRx=2,MRC)','sim(nTx=2,nRx=2,Alamouti)');
axis([0 25 10^-5 0.5])
set(gca, 'yscale', 'log', 'xlim', [0, 25], 'ylim', [1e-5 1]);
hh = gcf; grid on; hold on;
xlabel('Eb/No (dB)'); ylabel('BER'); set(hh,'NumberTitle','off');
set(hh, 'renderer', 'zbuffer'); set(hh,'Name','MQAM_BER');
title('Alamouti Scheme');